/**
 * Manages WebSocket connection for real-time updates
 */

export class WebSocketClient {
    constructor(state, eventBus) {
        this.state = state;
        this.eventBus = eventBus;

        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 3000;
        this.url = this.getWebSocketURL();
    }

    getWebSocketURL() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        return `${protocol}//${window.location.host}/ws/transfers-feed`;
    }

    connect() {
        try {
            console.log(`[WebSocket] Connecting to ${this.url}`);
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                console.log('[WebSocket] Connected to transfers feed');
                this.reconnectAttempts = 0;
                this.state.connection.webSocketConnected = true;

                // Send handshake
                try {
                    this.ws.send(JSON.stringify({
                        type: 'client_connected',
                        timestamp: Date.now()
                    }));
                } catch (error) {
                    console.log('[WebSocket] Could not send handshake:', error);
                }
            };

            this.ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    console.log('[WebSocket] Received message:', message);

                    // Forward to activity feed manager
                    this.eventBus.emit('activity:message', message);
                } catch (error) {
                    console.error('[WebSocket] Error parsing message:', error, event.data);
                }
            };

            this.ws.onerror = (error) => {
                console.error('[WebSocket] Connection error:', error);
            };

            this.ws.onclose = () => {
                console.log('[WebSocket] Connection closed');
                this.state.connection.webSocketConnected = false;
                this.attemptReconnect();
            };
        } catch (error) {
            console.error('[WebSocket] Failed to create connection:', error);
            this.attemptReconnect();
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts - 1);

            console.log(`[WebSocket] Reconnecting in ${Math.round(delay / 1000)}s (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

            setTimeout(() => this.connect(), delay);
        } else {
            console.warn('[WebSocket] Max reconnect attempts reached');
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
            this.state.connection.webSocketConnected = false;
        }
    }

    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }
}
