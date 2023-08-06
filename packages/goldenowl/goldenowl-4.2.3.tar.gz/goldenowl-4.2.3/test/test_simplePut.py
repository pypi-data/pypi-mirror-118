import pytest
import pandas as pd
import goldenowl.portfolio.holding as hd
import goldenowl.portfolio.simplePut as put
import goldenowl.asset.asset as at

def get_prdata():
    price_dict_raw ={
                '1992-11-23': 234.2,
                '1999-01-23': 34.2,
                '2000-10-03': 134.2,
                '2001-11-01': 333.9,
                '2002-11-23': 234.2,
                '2005-05-2': 100,
                '2012-01-23': 4000.0,
                };
    price_dict = {pd.to_datetime(key):val for key, val in price_dict_raw.items()} 
    tup = list(zip(price_dict.keys(), price_dict.values()));
    data = pd.DataFrame(tup, columns=['Date', 'Close']);
    data['Open'] = data['High'] = data['Low'] = 0;
    return at.Asset('Test', data);

def test_getValueOTM():
    price_dict = get_prdata();
    hldng =put.SimplePut('Test', price_dict, 200, '2004-01-01', 0.01);
    hldng.buyUnits(10, '1992-11-23');
    val = hldng.getValue('2012-01-23');
    assert (val) == 0, "OTM after expiry buyUnits failed"
    val = hldng.getValue('2001-12-03');
    assert (val) == pytest.approx(33.39,0.1), "OTM before expiry buyUnits failed"

def test_buyAmount():
    price_dict = get_prdata();
    hldng =put.SimplePut('Test', price_dict, 200, '2004-01-01', 0.01);
    hldng.buyAmount(23.4, '1992-11-23');
    val = hldng.getValue('2012-01-23');
    assert (val) == 0, "OTM after expiry buyUnits failed"
    val = hldng.getValue('2001-12-03');
    assert (val) == pytest.approx(33.39,0.1), "OTM before expiry buyUnits failed"

def test_sellAmount():
    price_dict = get_prdata();
    hldng =put.SimplePut('Test', price_dict, 200, '2005-06-01', 0.01);
    hldng.buyUnits(10, '1992-11-23');
    val = hldng.sellAmount(3.34, '2001-12-03');
    val = hldng.sellUnits(4, '2005-07-03');
    val = hldng.getValue('2012-01-23');
    assert (val) == pytest.approx(500,0.1), "ITM after expiry buyUnits failed"
    val = hldng.getValue('2000-12-03');
    assert (val) == pytest.approx(671.4,0.1), "ITM before expiry buyUnits failed"

def test_getValueITM():
    price_dict = get_prdata();
    hldng =put.SimplePut('Test', price_dict, 200, '2005-06-01', 0.01);
    hldng.buyUnits(10, '1992-11-23');
    val = hldng.getValue('2012-01-23');
    assert (val) == 1000, "ITM after expiry buyUnits failed"
    val = hldng.getValue('2000-12-03');
    assert (val) == pytest.approx(671.4,0.1), "ITM before expiry buyUnits failed"
