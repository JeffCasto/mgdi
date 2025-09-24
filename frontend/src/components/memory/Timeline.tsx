import React, { useEffect, useState } from "react";
import { api } from "../../services/api";

interface Memory {
  id: string;
  content: string;
  metadata: Record<string, unknown>;
  created_at: string;
  similarity?: number;
}

/**
 * A component to display a timeline of memories.
 *
 * This component fetches a timeline of memories from the API and displays
 * them in a list.
 *
 * @returns A component to display a timeline of memories.
 */
export default function Timeline() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTimeline();
  }, []);

  const loadTimeline = async () => {
    try {
      setLoading(true);
      const response = await api.get("/memory/timeline");
      setMemories(response.data);
    } catch (err) {
      setError("Failed to load timeline");
      console.error("Timeline error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return <div className="timeline-loading">Loading memories...</div>;
  if (error) return <div className="timeline-error">{error}</div>;

  return (
    <div className="timeline">
      <h3>Memory Timeline</h3>
      {memories.length === 0 ? (
        <div className="timeline-empty">No memories yet</div>
      ) : (
        <div className="timeline-entries">
          {memories.map((memory) => (
            <div key={memory.id} className="timeline-entry">
              <div className="timeline-date">
                {new Date(memory.created_at).toLocaleDateString()}
              </div>
              <div className="timeline-content">{memory.content}</div>
              {Object.keys(memory.metadata).length > 0 && (
                <div className="timeline-metadata">
                  {JSON.stringify(memory.metadata)}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <style>{`
        .timeline {
          padding: 1rem;
          max-height: 400px;
          overflow-y: auto;
        }
        .timeline-entry {
          border-left: 2px solid var(--accent);
          padding-left: 1rem;
          margin-bottom: 1rem;
        }
        .timeline-date {
          font-size: 0.8rem;
          color: var(--text-muted);
        }
        .timeline-content {
          margin: 0.5rem 0;
        }
        .timeline-metadata {
          font-size: 0.7rem;
          color: var(--text-muted);
          font-family: monospace;
        }
        /* TODO: Move to global CSS */
      `}</style>
    </div>
  );
}
