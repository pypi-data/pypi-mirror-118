import datetime
import pandas as pd
import numpy as np
from finlab import report
from finlab import data

def sim(position, resample=None, trade_at_price='close', position_limit=None, fee_ratio=1.425/1000,
        tax_ratio=3/1000, name=None, stop_loss=None, take_profit=None, day_trade=False, upload=True):

    # adjust for trading price
    if trade_at_price:
        price = data.get(f'etl:adj_{trade_at_price}')
    else:
        price = (data.get('etl:adj_close') + data.get('etl:adj_open'))/2
    position = position[position.index <= price.index[-1]]
    # resample dates
    if isinstance(resample, str):
        dates = pd.date_range(position.index[0], position.index[-1], freq=resample)
        next_trading_date = min(set(pd.date_range(position.index[0],
            datetime.datetime.now() + datetime.timedelta(days=720),
            freq=resample)) - set(dates))
    elif resample is None:
        dates = None
        next_trading_date = position.index[-1] + datetime.timedelta(days=1)


    # resize and normalize position
    positions = calculate_position(price, position, dates, position_limit)

    # add stop loss and take profits
    if stop_loss is not None or take_profit is not None:
      positions_reindex = positions.reindex(price.index, method='ffill').ffill()
      positions = positions_reindex * sl_tp_filter(positions > 0, stop_loss, take_profit, trade_at_price)
      positions.fillna(0, inplace=True)
    
    if day_trade == False:
      returns = calculate_capital(price, positions, fee_ratio, tax_ratio)
    else:
      returns = (data.get('etl:adj_close') / data.get('etl:adj_open') - 1
                ).shift(-1).reindex_like(positions).fillna(0)
      returns = (returns[positions != 0] * positions).sum(axis=1)
      returns = (returns[returns != 0] + 1 + (- 1.425/1000 * 2 - 3/1000) * positions.sum(axis=1)[returns != 0]).cumprod()


    # create report
    report_ret = report.Report(
            returns,positions, fee_ratio, tax_ratio,
            trade_at_price, next_trading_date)

    if not upload:
        return report_ret

    result = report_ret.upload(name)

    if 'status' in result and result['status'] == 'error':
        print('Fail to upload result to server')
        print('error message', result['message'])
        return report_ret

    try:
        url = 'https://ai.finlab.tw/strategy/?uid=' + result['uid'] + '&sid=' + result['strategy_id']
        from IPython.display import IFrame, display
        iframe = IFrame(url, width='100%', height=800)
        display(iframe)

    except Exception as e:
        pass

    return report_ret

def rebalance_dates(freq):
    if isinstance(freq, str):
        def f(start_date, end_date):
            return pd.date_range(start_date, end_date, freq=freq)
        return f
    elif isinstance(freq, pd.Series):
        def f(start_date, end_date):
            return pd.to_datetime(freq.loc[start_date, end_date].index)
    return f

def adjust_dates_to_index(creturn, dates):

    def to_buesiness_day(d):
        if d <= creturn.index[-1]:
            i = creturn.index.get_loc(d, method='bfill')
            ret = creturn.index[i]
        else:
            ret = None#creturn.index[-1]
        return ret

    return pd.DatetimeIndex(pd.Series(dates).apply(to_buesiness_day).dropna()).drop_duplicates()

def calculate_position(price, position, resample=None, position_limit=None):

    '''
    signalIn and signalOut are pandas dataframe, which indicate a stock should be
    bought or not.
    '''
    total_weight = position.abs().sum(axis=1).clip(1, None)
    position = position.div(total_weight, axis=0).fillna(0)

    if resample is not None:
        dates = adjust_dates_to_index(price, resample)
        position = position.reindex(dates, method='ffill').astype(float)

    # remove stock not traded
    position = position.loc[:, position.sum()!=0]

    # remove zero portfolio time period
    position = position.loc[(position.sum(axis=1) != 0).cumsum() != 0]
    return position.clip(0, position_limit)

def calculate_capital(price, position, fee_ratio, tax_ratio):

    # shapes of price and position should be the same
    # value of price and position should not be Nan
    stocks_list = position.columns.intersection(price.columns)
    adj_close = price.loc[position.index[0]:][stocks_list]
    position = position[stocks_list].reindex(adj_close.index, method='ffill').ffill().fillna(0)

    # forbid trading at the stock listing date
    position[adj_close.ffill().shift().isna() & adj_close.notna()] = 0

    # calculate position adjust dates
    periods = (position.diff().abs().sum(axis=1) > 0).cumsum()
    indexes = pd.Series(periods.index).groupby(periods.values).last()

    # calculate periodic returns
    selected_adj = (adj_close.shift(-2)/adj_close.shift(-1)).clip(0.9 ,1.1).fillna(1).groupby(periods).cumprod()
    selected_adj[((position == 0) | (selected_adj == 0))] = np.nan
    ret = (selected_adj * position).sum(axis=1) + (1 - position.sum(axis=1))

    # calculate cost
    pdiff = position.diff()
    pdiff[pdiff > 0] *= (fee_ratio)
    pdiff[pdiff < 0] *= (fee_ratio + tax_ratio)
    cost = pdiff.abs().sum(axis=1).shift()
    cost = cost.fillna(0)

    # calculate cummulation returns
    s = (pd.Series(ret.groupby(periods).last().values, indexes).reindex(ret.index).fillna(1).shift().cumprod() * ret)

    # consider cost
    cap = ((s.shift(-1) / s).shift(3) * (1-cost)).cumprod().fillna(1)

    return cap[cap.shift(-1, fill_value=1.1).fillna(1) != 1.0]


def sl_tp_filter(position, stop_loss=None, take_profit=None, trade_at_price='close'):
    """Add sl_sp condition in buy dataframe
    Args:
      position(dataframe): A dataframe of buy signals.
      stop_loss(float):Stop loss benchmark,ex:0.1(10%)
      take_profit(float):Stop profit benchmark,ex:0.1(10%)
      trade_at_price(str): Price option,close or open
    Returns:
        buy(dataframe):Intersection of signal list and stop-loss and stop-profit exit signals.

    """
    if (stop_loss is None) and (take_profit is None):
        return position

    adj_price = data.get(f'etl:adj_{trade_at_price}').ffill()
    adj_close_length = len(
        adj_price[(adj_price.index >= position.index[0]) & (adj_price.index <= position.index[-1])].index)
    position_length = len(position.index)

    def cal_func(buy):
        original_buy = buy.reindex(adj_price.index)
        buy = buy.reindex(adj_price.index, method='ffill')
        signal_df = (buy.shift() * adj_price).astype(float).fillna(0)
        returns = (signal_df / signal_df.shift()).replace(np.inf, 1).replace(0, np.nan).fillna(method='bfill', limit=1)
        returns = returns.cumprod()

        # get entry date
        entry_df = (buy - buy.shift()) > 0

        base_df = (returns * entry_df).replace(0, np.nan).fillna(method='ffill')
        hold_period_returns = (returns / base_df) - 1

        check_stop_loss, check_take_profit = True, True
        if stop_loss is not None:
            check_stop_loss = (hold_period_returns > -np.abs(stop_loss))

        if take_profit is not None:
            check_take_profit = (hold_period_returns < np.abs(take_profit))

        check_hold = (check_stop_loss & check_take_profit).cumsum()
        check_hold_period = (check_hold * entry_df).replace(0, np.nan).fillna(method='ffill')
        cont_hold = check_hold - check_hold_period

        cont_values_df = buy.cumsum()
        cont_df = (cont_values_df - (cont_values_df * entry_df).replace(0, np.nan).fillna(method='ffill'))
        check_cont = cont_df - cont_hold
        check_cont = check_cont.fillna(0)
        sl_tp_df = check_cont < 1

        if adj_close_length == position_length:
            return sl_tp_df & buy
        else:
            return (sl_tp_df & buy) | original_buy

    result = cal_func(position)
    check_new_sig = pd.DataFrame()

    # returns-base should be restarted when exited signals appeared during consecutive selections
    while result.equals(check_new_sig) is False:
        check_new_sig = result.copy()
        mid = (result - result.shift()) * (result - result.shift(-1)) > 0
        new_buy = mid.reindex(position.index)
        sig_mid = cal_func(new_buy)
        result = result | sig_mid

    return result
