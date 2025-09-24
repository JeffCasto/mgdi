import React from "react";
import MessageList from "./components/chat/MessageList";
import MessageComposer from "./components/chat/MessageComposer";
import Sidebar from "./components/sidebar/Sidebar";
import StreamingIndicator from "./components/common/StreamingIndicator";
import SettingsModal from "./components/modals/SettingsModal";
import "./styles/theme.css";

/**
 * The main application component.
 *
 * This component lays out the main structure of the application, including the
 * sidebar, message list, message composer, and settings modal.
 *
 * @returns The main application component.
 */
export default function App() {
  return (
    <div
      style={{ display: "flex", height: "100vh", background: "var(--surface)" }}
    >
      <Sidebar />
      <main style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <MessageList />
        <StreamingIndicator />
        <MessageComposer />
      </main>
      <SettingsModal />
    </div>
  );
}
