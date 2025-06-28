from typing import TYPE_CHECKING, Callable
import time

if TYPE_CHECKING:
    from .client import IGClient
from lightstreamer.client import LightstreamerClient, Subscription
import threading


class IGStreamingClient:
    """Streaming client for IG using Lightstreamer SDK."""

    def __init__(
        self,
        client: "IGClient",
        reconnect: bool = True,
        reconnect_delay: int = 5,
    ) -> None:
        """Initialize IGStreamingClient with authenticated IGClient.
        :param reconnect: If True, automatically reconnect on disconnect.
        :param reconnect_delay: Seconds to wait before reconnecting.
        """
        self.client = client
        self._ls_client = None
        self._subscriptions = {}
        self._lock = threading.Lock()
        self.account_id = self.client.session_data.get("currentAccountId")
        self._reconnect = reconnect
        self._reconnect_delay = reconnect_delay
        self._should_run = True

    def start(self) -> None:
        """Start Lightstreamer connection. Reconnects if enabled."""
        ls_endpoint = self.client.session_data["lightstreamerEndpoint"]
        if not ls_endpoint:
            ls_endpoint = "https://push.lightstreamer.com"
        print("Using Lightstreamer endpoint:", ls_endpoint)
        account_id = self.account_id
        cst = self.client.session.headers.get("CST")
        xst = self.client.session.headers.get("X-SECURITY-TOKEN")
        if not (cst and xst):
            raise RuntimeError(
                "Missing CST or X-SECURITY-TOKEN. Make sure you are logged in."
            )
        self._ls_client = LightstreamerClient(ls_endpoint, account_id)
        self._ls_client.connectionDetails.setPassword(f"CST-{cst}|XST-{xst}")
        self._ls_client.connectionDetails.setAdapterSet("DEFAULT")

        def on_status_change(status):
            print(f"[Lightstreamer] Connection status: {status}")
            if (
                status.startswith("DISCONNECTED")
                and self._reconnect
                and self._should_run
            ):
                print(
                    "[Lightstreamer] Disconnected. Attempting to reconnect in",
                    self._reconnect_delay,
                    "seconds...",
                )
                time.sleep(self._reconnect_delay)
                self._reconnect_subscriptions()

        def on_server_error(code, msg):
            print(f"[Lightstreamer] Server error: {code} - {msg}")

        self._ls_client.addListener(
            type(
                "_LSListener",
                (),
                {
                    "onStatusChange": staticmethod(on_status_change),
                    "onServerError": staticmethod(on_server_error),
                },
            )()
        )
        self._ls_client.connect()

    def _reconnect_subscriptions(self):
        """Reconnects the Lightstreamer client and all active subscriptions."""
        try:
            self._ls_client.disconnect()
        except Exception:
            pass
        self._ls_client.connect()
        # Re-subscribe to all items
        with self._lock:
            for item, sub in self._subscriptions.items():
                self._ls_client.subscribe(sub)
        print("[Lightstreamer] Reconnected and re-subscribed to all items.")

    def subscribe(
        self,
        item: str,
        mode: str,
        fields: list[str],
        callback: Callable[[dict], None],  # expects callback(data)
        adapter: str = None,
    ) -> None:
        """
        Subscribe to any Lightstreamer item (generic).
        The callback will be called as callback(data) for item updates.
        """
        subscription = Subscription(mode=mode, items=[item], fields=fields)
        if adapter:
            subscription.setDataAdapter(adapter)

        class _Listener:
            @staticmethod
            def onItemUpdate(item_update):
                try:
                    data = {
                        field: item_update.getValue(field) for field in fields
                    }
                    callback(data)
                except Exception as e:
                    print(f"[ERROR] Exception in onItemUpdate callback: {e}")

            @staticmethod
            def onSubscription():
                print(f"[Subscription] Subscribed to {item}")

            @staticmethod
            def onSubscriptionError(code, message):
                print(f"[Subscription] Error for {item}: {code} - {message}")

            @staticmethod
            def onUnsubscription():
                print(f"[Subscription] Unsubscribed from {item}")

        subscription.addListener(_Listener())
        with self._lock:
            self._ls_client.subscribe(subscription)
            self._subscriptions[item] = subscription

    # Convenience methods for all IG streaming types
    def subscribe_price(
        self, epic: str, fields: list[str], callback: Callable[[dict], None]
    ) -> None:
        """Subscribe to price updates for a given epic."""
        item = f"PRICE:{self.account_id}:{epic}"
        self.subscribe(item, "MERGE", fields, callback, adapter="Pricing")

    def unsubscribe_price(self, epic: str) -> None:
        """Unsubscribe from price updates for a given epic."""
        item = f"PRICE:{self.account_id}:{epic}"
        with self._lock:
            sub = self._subscriptions.pop(item, None)
            if sub:
                self._ls_client.unsubscribe(sub)

    def subscribe_account(
        self, fields: list[str], callback: Callable[[dict], None]
    ) -> None:
        """Subscribe to account updates."""
        item = f"ACCOUNT:{self.account_id}"
        self.subscribe(item, "MERGE", fields, callback)

    def unsubscribe_account(self) -> None:
        """Unsubscribe from account updates."""
        item = f"ACCOUNT:{self.account_id}"
        with self._lock:
            sub = self._subscriptions.pop(item, None)
            if sub:
                self._ls_client.unsubscribe(sub)

    def subscribe_trade(
        self, fields: list[str], callback: Callable[[dict], None]
    ) -> None:
        """Subscribe to trade updates."""
        item = f"TRADE:{self.account_id}"
        self.subscribe(item, "DISTINCT", fields, callback)

    def unsubscribe_trade(self) -> None:
        """Unsubscribe from trade updates."""
        item = f"TRADE:{self.account_id}"
        with self._lock:
            sub = self._subscriptions.pop(item, None)
            if sub:
                self._ls_client.unsubscribe(sub)

    def subscribe_chart_tick(
        self, epic: str, fields: list[str], callback: Callable[[dict], None]
    ) -> None:
        """Subscribe to chart tick updates."""
        item = f"CHART:{epic}:TICK"
        self.subscribe(item, "DISTINCT", fields, callback)

    def unsubscribe_chart_tick(self, epic: str) -> None:
        """Unsubscribe from chart tick updates."""
        item = f"CHART:{epic}:TICK"
        with self._lock:
            sub = self._subscriptions.pop(item, None)
            if sub:
                self._ls_client.unsubscribe(sub)

    def subscribe_chart_candle(
        self,
        epic: str,
        scale: str,
        fields: list[str],
        callback: Callable[[dict], None],
    ) -> None:
        """Subscribe to chart candle updates."""
        item = f"CHART:{epic}:{scale}"
        self.subscribe(item, "MERGE", fields, callback)

    def unsubscribe_chart_candle(self, epic: str, scale: str) -> None:
        """Unsubscribe from chart candle updates."""
        item = f"CHART:{epic}:{scale}"
        with self._lock:
            sub = self._subscriptions.pop(item, None)
            if sub:
                self._ls_client.unsubscribe(sub)

    def unsubscribe(self, item: str) -> None:
        """Unsubscribe from any Lightstreamer item by item string."""
        with self._lock:
            sub = self._subscriptions.pop(item, None)
            if sub:
                self._ls_client.unsubscribe(sub)

    def stop(self) -> None:
        """Disconnect from Lightstreamer server and stop reconnect attempts."""
        self._should_run = False
        if self._ls_client:
            self._ls_client.disconnect()
