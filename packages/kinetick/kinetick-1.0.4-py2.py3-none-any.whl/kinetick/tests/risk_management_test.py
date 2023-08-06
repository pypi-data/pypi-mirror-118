from kinetick.risk_assessor import RiskAssessor as RiskManager

def getInstance():
    risk_manager = RiskManager(initial_capital=100000, risk2reward=1, risk_per_trade=100, initial_margin=100)
    return risk_manager

def test_singleton_property():
    risk_manager = RiskManager.get_default_instance()
    rm = RiskManager(initial_capital=100)
    rm2 = risk_manager
    assert rm.capital == rm2.capital


def test_trade():
    risk_manager = getInstance()
    trade = risk_manager.create_position(82.45, 80.05)
    assert trade.direction == "LONG"
    assert "{:.2f}".format(trade.target) == str(84.85)
    assert trade.quantity == 41


def test_trade_entry():
    risk_manager = getInstance()
    trade = risk_manager.create_position(82.45, 80.05)
    risk_manager.enter_position(trade)
    assert len(risk_manager.active_positions) == 1
    assert risk_manager.available_margin < 2


def foo():
    pass


def test_trade_exit():
    risk_manager = getInstance()
    trade = risk_manager.create_position(82.45, 80.05)
    risk_manager.enter_position(trade)
    trade.exit_price = 84.85
    trade.save = foo
    trade = risk_manager.exit_position(trade)
    assert len(risk_manager.active_positions) == 0
    assert risk_manager.available_margin == 100.0
    assert risk_manager.initial_margin == 100
    assert trade.realized_pnl > 98


if __name__ == "__main__":
    test_singleton_property()
    test_trade()
    test_trade_entry()
    test_trade_exit()
