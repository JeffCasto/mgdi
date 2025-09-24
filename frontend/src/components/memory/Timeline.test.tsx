import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { jest } from "@jest/globals";
import Timeline from "./Timeline";
import { api } from "../../services/api";

// Mock API calls
jest.mock("../../services/api", () => ({
  api: {
    get: jest.fn(),
  },
}));

const mockApi = api as jest.Mocked<typeof api>;

const mockMemories = [
  {
    id: "1",
    content: "User prefers dark theme",
    metadata: { type: "preference" },
    created_at: "2024-01-01T00:00:00Z",
  },
  {
    id: "2",
    content: "Discussed React optimization",
    metadata: { topic: "performance" },
    created_at: "2024-01-02T00:00:00Z",
  },
];

describe("Timeline Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders loading state initially", () => {
    mockApi.get.mockImplementation(() => new Promise(() => {})); // Never resolves
    render(<Timeline />);
    expect(screen.getByText("Loading memories...")).toBeInTheDocument();
  });

  test("renders timeline with memories", async () => {
    mockApi.get.mockResolvedValue({ data: mockMemories });

    render(<Timeline />);

    await waitFor(() => {
      expect(screen.getByText("Memory Timeline")).toBeInTheDocument();
      expect(screen.getByText("User prefers dark theme")).toBeInTheDocument();
      expect(
        screen.getByText("Discussed React optimization"),
      ).toBeInTheDocument();
    });

    expect(mockApi.get).toHaveBeenCalledWith("/memory/timeline");
  });

  test("renders empty state when no memories", async () => {
    mockApi.get.mockResolvedValue({ data: [] });

    render(<Timeline />);

    await waitFor(() => {
      expect(screen.getByText("No memories yet")).toBeInTheDocument();
    });
  });

  test("renders error state on API failure", async () => {
    mockApi.get.mockRejectedValue(new Error("API Error"));

    render(<Timeline />);

    await waitFor(() => {
      expect(screen.getByText("Failed to load timeline")).toBeInTheDocument();
    });
  });

  test("displays memory metadata when present", async () => {
    mockApi.get.mockResolvedValue({ data: mockMemories });

    render(<Timeline />);

    await waitFor(() => {
      expect(screen.getByText('{"type":"preference"}')).toBeInTheDocument();
      expect(screen.getByText('{"topic":"performance"}')).toBeInTheDocument();
    });
  });

  test("formats dates correctly", async () => {
    mockApi.get.mockResolvedValue({ data: mockMemories });

    render(<Timeline />);

    await waitFor(() => {
      expect(screen.getByText("1/1/2024")).toBeInTheDocument();
      expect(screen.getByText("1/2/2024")).toBeInTheDocument();
    });
  });
});

// TODO(codex): Add integration tests with real API endpoints
// TODO(codex): Test auth-gated memory access
// TODO(codex): Test memory search functionality
