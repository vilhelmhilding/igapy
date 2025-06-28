import argparse
import json
from .client import IGClient
from .accounts import Accounts
from .markets import Markets
from .orders import Orders
from .prices import Prices
from .sentiment import Sentiment
from .history import History
from .repeat import RepeatDealWindow
from .watchlists import Watchlists
from .costs import CostsAndCharges
from .operations import Operations
from .session import SessionAPI


def main() -> None:
    """IG API CLI entry point."""
    parser = argparse.ArgumentParser(prog="igapy", description="IG API CLI")
    parser.add_argument("--api-key", required=True, help="IG API key")
    parser.add_argument("--username", required=True, help="IG username")
    parser.add_argument("--password", required=True, help="IG password")
    parser.add_argument(
        "--demo", action="store_true", help="Use IG demo environment"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Accounts
    accounts_parser = subparsers.add_parser(
        "accounts", help="Accounts operations"
    )
    accounts_sub = accounts_parser.add_subparsers(dest="accounts_cmd")
    accounts_sub.add_parser("list", help="List all accounts")
    acc_pref = accounts_sub.add_parser(
        "get-preferences", help="Get account preferences"
    )
    acc_pref.add_argument("--account-id", required=True)
    acc_upd = accounts_sub.add_parser(
        "update-preferences", help="Update account preferences"
    )
    acc_upd.add_argument("--account-id", required=True)
    acc_upd.add_argument(
        "--preferences", required=True, help="Preferences as JSON string"
    )

    # Markets
    markets_parser = subparsers.add_parser(
        "markets", help="Markets operations"
    )
    markets_sub = markets_parser.add_subparsers(dest="markets_cmd")
    mkt_search = markets_sub.add_parser("search", help="Search markets")
    mkt_search.add_argument("--search-term", required=True)
    mkt_details = markets_sub.add_parser(
        "get-details", help="Get market details"
    )
    mkt_details.add_argument("--epic", required=True)
    mkt_bulk = markets_sub.add_parser("get-bulk", help="Get multiple markets")
    mkt_bulk.add_argument(
        "--epics", required=True, help="Comma-separated epics"
    )
    markets_sub.add_parser("navigation", help="Get market navigation")
    mkt_subnodes = markets_sub.add_parser(
        "sub-nodes", help="Get market sub nodes"
    )
    mkt_subnodes.add_argument("--node-id", required=True)

    # Prices
    prices_parser = subparsers.add_parser("prices", help="Prices operations")
    prices_sub = prices_parser.add_subparsers(dest="prices_cmd")
    p_basic = prices_sub.add_parser("get", help="Get prices")
    p_basic.add_argument("--epic", required=True)
    p_basic.add_argument("--resolution", default="MINUTE")
    p_basic.add_argument("--from-date")
    p_basic.add_argument("--to-date")
    p_basic.add_argument("--max-points", type=int)
    p_basic.add_argument("--page-size", type=int)
    p_basic.add_argument("--page-number", type=int, default=1)
    p_num = prices_sub.add_parser(
        "num-points", help="Get prices by num points"
    )
    p_num.add_argument("--epic", required=True)
    p_num.add_argument("--resolution", required=True)
    p_num.add_argument("--num-points", type=int, required=True)
    p_range = prices_sub.add_parser(
        "date-range", help="Get prices by date range"
    )
    p_range.add_argument("--epic", required=True)
    p_range.add_argument("--resolution", required=True)
    p_range.add_argument("--start", required=True)
    p_range.add_argument("--end", required=True)
    p_query = prices_sub.add_parser(
        "query-range", help="Get prices by query range"
    )
    p_query.add_argument("--epic", required=True)
    p_query.add_argument("--resolution", required=True)
    p_query.add_argument("--start", required=True)
    p_query.add_argument("--end", required=True)

    # Orders (add get/update/delete single position, create working order)
    orders_parser = subparsers.add_parser("orders", help="Orders operations")
    orders_sub = orders_parser.add_subparsers(dest="orders_cmd")
    o_create = orders_sub.add_parser("create", help="Create OTC position")
    o_create.add_argument(
        "--order", required=True, help="Order as JSON string"
    )
    orders_sub.add_parser("positions", help="Get positions")
    o_get = orders_sub.add_parser(
        "get-position", help="Get position by deal ID"
    )
    o_get.add_argument("--deal-id", required=True)
    o_update = orders_sub.add_parser(
        "update-position", help="Update position by deal ID"
    )
    o_update.add_argument("--deal-id", required=True)
    o_update.add_argument(
        "--data", required=True, help="Update data as JSON string"
    )
    orders_sub.add_parser("working", help="Get working orders")
    o_create_working = orders_sub.add_parser(
        "create-working", help="Create working order"
    )
    o_create_working.add_argument(
        "--order", required=True, help="Order as JSON string"
    )
    o_delete = orders_sub.add_parser(
        "delete-working", help="Delete working order"
    )
    o_delete.add_argument("--deal-id", required=True)
    o_conf = orders_sub.add_parser("confirms", help="Get confirms")
    o_conf.add_argument("--deal-reference", required=True)

    # Sentiment
    sentiment_parser = subparsers.add_parser(
        "sentiment", help="Sentiment operations"
    )
    sentiment_sub = sentiment_parser.add_subparsers(dest="sentiment_cmd")
    s_list = sentiment_sub.add_parser("list", help="List client sentiment")
    s_list.add_argument(
        "--market-ids", required=True, help="Comma-separated market ids"
    )
    s_get = sentiment_sub.add_parser("get", help="Get client sentiment")
    s_get.add_argument("--market-id", required=True)
    s_related = sentiment_sub.add_parser(
        "related", help="Get related sentiment"
    )
    s_related.add_argument("--market-id", required=True)

    # History
    history_parser = subparsers.add_parser(
        "history", help="History operations"
    )
    history_sub = history_parser.add_subparsers(dest="history_cmd")
    history_sub.add_parser("activity", help="Get activity")
    h_period = history_sub.add_parser(
        "activity-period", help="Get activity by period"
    )
    h_period.add_argument("--last-period", required=True)
    h_range = history_sub.add_parser(
        "activity-range", help="Get activity by date range"
    )
    h_range.add_argument("--from-date", required=True)
    h_range.add_argument("--to-date", required=True)
    history_sub.add_parser("transactions", help="Get transactions")
    t_period = history_sub.add_parser(
        "transactions-period", help="Get transactions by period"
    )
    t_period.add_argument("--last-period", required=True)
    t_range = history_sub.add_parser(
        "transactions-range", help="Get transactions by date range"
    )
    t_range.add_argument("--from-date", required=True)
    t_range.add_argument("--to-date", required=True)
    t_type_period = history_sub.add_parser(
        "transactions-type-period", help="Get transactions by type and period"
    )
    t_type_period.add_argument("--transaction-type", required=True)
    t_type_period.add_argument("--last-period", required=True)
    t_type_range = history_sub.add_parser(
        "transactions-type-range",
        help="Get transactions by type and date range",
    )
    t_type_range.add_argument("--transaction-type", required=True)
    t_type_range.add_argument("--from-date", required=True)
    t_type_range.add_argument("--to-date", required=True)

    # Repeat
    repeat_parser = subparsers.add_parser("repeat", help="Repeat deal window")
    repeat_parser.add_subparsers(dest="repeat_cmd").add_parser(
        "get", help="Get repeat deal window"
    )

    # Watchlists
    watchlists_parser = subparsers.add_parser(
        "watchlists", help="Watchlists operations"
    )
    watchlists_sub = watchlists_parser.add_subparsers(dest="watchlists_cmd")
    watchlists_sub.add_parser("list", help="List watchlists")
    w_create = watchlists_sub.add_parser("create", help="Create watchlist")
    w_create.add_argument(
        "--data", required=True, help="Watchlist data as JSON string"
    )
    w_get = watchlists_sub.add_parser("get", help="Get watchlist")
    w_get.add_argument("--watchlist-id", required=True)
    w_delete = watchlists_sub.add_parser("delete", help="Delete watchlist")
    w_delete.add_argument("--watchlist-id", required=True)
    w_add = watchlists_sub.add_parser(
        "add-market", help="Add market to watchlist"
    )
    w_add.add_argument("--watchlist-id", required=True)
    w_add.add_argument("--epic", required=True)
    w_remove = watchlists_sub.add_parser(
        "remove-market", help="Remove market from watchlist"
    )
    w_remove.add_argument("--watchlist-id", required=True)
    w_remove.add_argument("--epic", required=True)

    # Costs (add open)
    costs_parser = subparsers.add_parser(
        "costs", help="Costs and charges operations"
    )
    costs_sub = costs_parser.add_subparsers(dest="costs_cmd")
    c_close = costs_sub.add_parser("close", help="Close costs")
    c_close.add_argument("--data", required=True, help="Data as JSON string")
    c_open = costs_sub.add_parser("open", help="Open costs")
    c_open.add_argument("--data", required=True, help="Data as JSON string")
    c_edit = costs_sub.add_parser("edit", help="Edit costs")
    c_edit.add_argument("--data", required=True, help="Data as JSON string")
    c_pdf = costs_sub.add_parser("pdf", help="Download PDF")
    c_pdf.add_argument("--reference", required=True)
    c_hist = costs_sub.add_parser("history", help="History costs")
    c_hist.add_argument("--from-date", required=True)
    c_hist.add_argument("--to-date", required=True)

    # Operations
    operations_parser = subparsers.add_parser("operations", help="Operations")
    operations_sub = operations_parser.add_subparsers(dest="operations_cmd")
    operations_sub.add_parser("list", help="List applications")
    o_update = operations_sub.add_parser("update", help="Update application")
    o_update.add_argument("--data", required=True, help="Data as JSON string")
    operations_sub.add_parser("disable", help="Disable application")

    # Session
    session_parser = subparsers.add_parser(
        "session", help="Session operations"
    )
    session_sub = session_parser.add_subparsers(dest="session_cmd")
    s_details = session_sub.add_parser("details", help="Get session details")
    s_details.add_argument("--fetch-session-tokens", action="store_true")
    session_sub.add_parser("logout", help="Logout")
    session_sub.add_parser("encryption-key", help="Get encryption key")
    s_refresh = session_sub.add_parser("refresh", help="Refresh session")
    s_refresh.add_argument("--refresh-token", required=True)
    s_switch = session_sub.add_parser("switch-account", help="Switch account")
    s_switch.add_argument("--account-id", required=True)
    s_switch.add_argument("--default-account", action="store_true")

    args = parser.parse_args()

    client = IGClient(
        api_key=args.api_key,
        username=args.username,
        password=args.password,
        is_demo=args.demo,
    )
    client.login()

    if args.command == "accounts":
        acc = Accounts(client)
        if args.accounts_cmd == "list":
            print(json.dumps(acc.list_accounts(), indent=2))
        elif args.accounts_cmd == "get-preferences":
            print(json.dumps(acc.get_preferences(), indent=2))
        elif args.accounts_cmd == "update-preferences":
            prefs = json.loads(args.preferences)
            print(json.dumps(acc.update_preferences(prefs), indent=2))
        else:
            print("Unknown accounts command.")

    elif args.command == "markets":
        mkt = Markets(client)
        if args.markets_cmd == "search":
            print(json.dumps(mkt.search_markets(args.search_term), indent=2))
        elif args.markets_cmd == "get-details":
            print(json.dumps(mkt.get_market_details(args.epic), indent=2))
        elif args.markets_cmd == "get-bulk":
            epics = args.epics.split(",")
            print(json.dumps(mkt.get_markets_bulk(epics), indent=2))
        elif args.markets_cmd == "navigation":
            print(json.dumps(mkt.get_market_navigation(), indent=2))
        elif args.markets_cmd == "sub-nodes":
            print(json.dumps(mkt.get_market_subnodes(args.node_id), indent=2))
        else:
            print("Unknown markets command.")

    elif args.command == "prices":
        prc = Prices(client)
        if args.prices_cmd == "get":
            print(
                json.dumps(
                    prc.get_prices(
                        args.epic,
                        args.resolution,
                        args.from_date,
                        args.to_date,
                        args.max_points,
                        args.page_size,
                        args.page_number,
                    ),
                    indent=2,
                )
            )
        elif args.prices_cmd == "num-points":
            print(
                json.dumps(
                    prc.get_prices_by_num_points(
                        args.epic, args.resolution, args.num_points
                    ),
                    indent=2,
                )
            )
        elif args.prices_cmd == "date-range":
            print(
                json.dumps(
                    prc.get_prices_by_date_range(
                        args.epic, args.resolution, args.start, args.end
                    ),
                    indent=2,
                )
            )
        elif args.prices_cmd == "query-range":
            print(
                json.dumps(
                    prc.get_prices_by_query_range(
                        args.epic, args.resolution, args.start, args.end
                    ),
                    indent=2,
                )
            )
        else:
            print("Unknown prices command.")

    elif args.command == "orders":
        ords = Orders(client)
        if args.orders_cmd == "create":
            order = json.loads(args.order)
            print(json.dumps(ords.create_otc_position(order), indent=2))
        elif args.orders_cmd == "positions":
            print(json.dumps(ords.get_positions(), indent=2))
        elif args.orders_cmd == "get-position":
            print(json.dumps(ords.get_position(args.deal_id), indent=2))
        elif args.orders_cmd == "update-position":
            data = json.loads(args.data)
            print(
                json.dumps(ords.update_position(args.deal_id, data), indent=2)
            )
        elif args.orders_cmd == "working":
            print(json.dumps(ords.get_working_orders(), indent=2))
        elif args.orders_cmd == "create-working":
            order = json.loads(args.order)
            print(json.dumps(ords.create_working_order(order), indent=2))
        elif args.orders_cmd == "delete-working":
            print(
                json.dumps(ords.delete_working_order(args.deal_id), indent=2)
            )
        elif args.orders_cmd == "confirms":
            print(json.dumps(ords.get_confirms(args.deal_reference), indent=2))
        else:
            print("Unknown orders command.")

    elif args.command == "sentiment":
        sent = Sentiment(client)
        if args.sentiment_cmd == "list":
            ids = args.market_ids.split(",")
            print(json.dumps(sent.list_client_sentiment(ids), indent=2))
        elif args.sentiment_cmd == "get":
            print(
                json.dumps(sent.get_client_sentiment(args.market_id), indent=2)
            )
        elif args.sentiment_cmd == "related":
            print(
                json.dumps(
                    sent.get_related_sentiment(args.market_id), indent=2
                )
            )
        else:
            print("Unknown sentiment command.")

    elif args.command == "history":
        hist = History(client)
        if args.history_cmd == "activity":
            print(json.dumps(hist.get_activity(), indent=2))
        elif args.history_cmd == "activity-period":
            print(
                json.dumps(
                    hist.get_activity_by_period(args.last_period), indent=2
                )
            )
        elif args.history_cmd == "activity-range":
            print(
                json.dumps(
                    hist.get_activity_by_date_range(
                        args.from_date, args.to_date
                    ),
                    indent=2,
                )
            )
        elif args.history_cmd == "transactions":
            print(json.dumps(hist.get_transactions(), indent=2))
        elif args.history_cmd == "transactions-period":
            print(
                json.dumps(
                    hist.get_transactions_by_period(args.last_period), indent=2
                )
            )
        elif args.history_cmd == "transactions-range":
            print(
                json.dumps(
                    hist.get_transactions_by_date_range(
                        args.from_date, args.to_date
                    ),
                    indent=2,
                )
            )
        elif args.history_cmd == "transactions-type-period":
            print(
                json.dumps(
                    hist.get_transactions_by_type_and_period(
                        args.transaction_type, args.last_period
                    ),
                    indent=2,
                )
            )
        elif args.history_cmd == "transactions-type-range":
            print(
                json.dumps(
                    hist.get_transactions_by_type_and_date_range(
                        args.transaction_type, args.from_date, args.to_date
                    ),
                    indent=2,
                )
            )
        else:
            print("Unknown history command.")

    elif args.command == "repeat":
        rep = RepeatDealWindow(client)
        if args.repeat_cmd == "get":
            print(json.dumps(rep.get_repeat_deal_window(), indent=2))
        else:
            print("Unknown repeat command.")

    elif args.command == "watchlists":
        wl = Watchlists(client)
        if args.watchlists_cmd == "list":
            print(json.dumps(wl.list_watchlists(), indent=2))
        elif args.watchlists_cmd == "create":
            data = json.loads(args.data)
            print(json.dumps(wl.create_watchlist(data), indent=2))
        elif args.watchlists_cmd == "get":
            print(json.dumps(wl.get_watchlist(args.watchlist_id), indent=2))
        elif args.watchlists_cmd == "delete":
            print(json.dumps(wl.delete_watchlist(args.watchlist_id), indent=2))
        elif args.watchlists_cmd == "add-market":
            print(
                json.dumps(
                    wl.add_market_to_watchlist(args.watchlist_id, args.epic),
                    indent=2,
                )
            )
        elif args.watchlists_cmd == "remove-market":
            print(
                json.dumps(
                    wl.remove_market_from_watchlist(
                        args.watchlist_id, args.epic
                    ),
                    indent=2,
                )
            )
        else:
            print("Unknown watchlists command.")

    elif args.command == "costs":
        costs = CostsAndCharges(client)
        if args.costs_cmd == "close":
            data = json.loads(args.data)
            print(json.dumps(costs.close_costs(data), indent=2))
        elif args.costs_cmd == "open":
            data = json.loads(args.data)
            print(json.dumps(costs.open_costs(data), indent=2))
        elif args.costs_cmd == "edit":
            data = json.loads(args.data)
            print(json.dumps(costs.edit_costs(data), indent=2))
        elif args.costs_cmd == "pdf":
            print(json.dumps(costs.download_pdf(args.reference), indent=2))
        elif args.costs_cmd == "history":
            print(
                json.dumps(
                    costs.history_costs(args.from_date, args.to_date), indent=2
                )
            )
        else:
            print("Unknown costs command.")

    elif args.command == "operations":
        ops = Operations(client)
        if args.operations_cmd == "list":
            print(json.dumps(ops.list_applications(), indent=2))
        elif args.operations_cmd == "update":
            data = json.loads(args.data)
            print(json.dumps(ops.update_application(data), indent=2))
        elif args.operations_cmd == "disable":
            print(json.dumps(ops.disable_application(), indent=2))
        else:
            print("Unknown operations command.")

    elif args.command == "session":
        sess = SessionAPI(client)
        if args.session_cmd == "details":
            print(
                json.dumps(
                    sess.get_session_details(args.fetch_session_tokens),
                    indent=2,
                )
            )
        elif args.session_cmd == "logout":
            print(json.dumps(sess.logout(), indent=2))
        elif args.session_cmd == "encryption-key":
            print(json.dumps(sess.get_encryption_key(), indent=2))
        elif args.session_cmd == "refresh":
            print(
                json.dumps(sess.refresh_session(args.refresh_token), indent=2)
            )
        elif args.session_cmd == "switch-account":
            print(
                json.dumps(
                    sess.switch_account(args.account_id, args.default_account),
                    indent=2,
                )
            )
        else:
            print("Unknown session command.")
    else:
        parser.print_help()
