/**
 * @file websocket-client.js
 * @description WebSocket client for real-time backup updates
 */

// =====================================================================
// --- WEBSOCKET CLIENT FOR TRANSFERS FEED ---
// =====================================================================

class BackupStatusClient {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 3000; // 3 seconds
        this.url = this.getWebSocketURL();
        this.isConnecting = false;
        this.pendingMessages = [];

        // Auto-connect on creation
        this.connect();
    }

    getWebSocketURL() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        return `${protocol}//${window.location.host}/ws/transfers-feed`;
    }

    connect() {
        if (this.isConnecting) return;

        this.isConnecting = true;

        try {
            console.log(`[WebSocket] Attempting to connect to ${this.url}`);
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                console.log('[WebSocket] ✓ Connected to transfers feed');
                this.reconnectAttempts = 0;
                this.isConnecting = false;

                // Send any pending messages
                this.flushPendingMessages();
            };

            this.ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    console.log('[WebSocket] Received message:', message);

                    // Handle message (will be imported from dashboard.js later)
                    if (window.ActivityFeedManager && window.ActivityFeedManager.handleMessage) {
                        window.ActivityFeedManager.handleMessage(message);
                    }
                } catch (e) {
                    console.error('[WebSocket] Error parsing message:', e, event.data);
                }
            };

            this.ws.onerror = (error) => {
                console.error('[WebSocket] Connection error:', error);
                this.isConnecting = false;
            };

            this.ws.onclose = (event) => {
                console.log(`[WebSocket] Connection closed. Code: ${event.code}, Reason: ${event.reason}`);
                this.isConnecting = false;
                this.attemptReconnect();
            };
        } catch (error) {
            console.error('[WebSocket] Failed to create connection:', error);
            this.isConnecting = false;
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
            console.warn('[WebSocket] Max reconnect attempts reached. Activity feed will not receive live updates.');
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close(1000, 'Client disconnecting');
            this.ws = null;
        }
        this.isConnecting = false;
        this.pendingMessages = [];
    }

    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    send(message) {
        if (this.isConnected()) {
            try {
                this.ws.send(JSON.stringify(message));
            } catch (e) {
                console.warn('[WebSocket] Failed to send message:', e);
                this.pendingMessages.push(message);
            }
        } else {
            this.pendingMessages.push(message);
        }
    }

    flushPendingMessages() {
        while (this.pendingMessages.length > 0 && this.isConnected()) {
            const message = this.pendingMessages.shift();
            try {
                this.ws.send(JSON.stringify(message));
            } catch (e) {
                console.warn('[WebSocket] Failed to send pending message:', e);
                this.pendingMessages.unshift(message);
                break;
            }
        }
    }
}

// =====================================================================
// --- EXPORTS ---
// =====================================================================

export { BackupStatusClient };

// Make globally available
window.BackupStatusClient = BackupStatusClient;
