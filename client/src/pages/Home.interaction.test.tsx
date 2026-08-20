/* @vitest-environment jsdom */
import React from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const state = vi.hoisted(() => ({
  auth: { loading: false, isAuthenticated: true, error: null as Error | null },
  mutation: { isPending: false, isSuccess: true, data: { diagnosticId: "diag-8", version: 8 } as { diagnosticId: string; version: number } | undefined },
}));

vi.mock("@/_core/hooks/useAuth", () => ({ useAuth: () => state.auth }));
vi.mock("@/const", () => ({ startLogin: vi.fn() }));
vi.mock("@/components/DashboardLayout", async () => {
  const ReactModule = await import("react");
  return { default: ({ children }: { children: React.ReactNode }) => ReactModule.createElement("div", null, children) };
});
vi.mock("@/lib/trpc", () => ({
  trpc: {
    useUtils: () => ({ analysis: { listProjects: { invalidate: vi.fn() } } }),
    analysis: {
      listProjects: { useQuery: () => ({ data: [], isLoading: false, isError: false }) },
      getDiagnostic: { useQuery: () => ({ data: undefined, isFetching: false, isError: false }) },
      analyzeWorkbook: { useMutation: () => ({ ...state.mutation, mutate: vi.fn() }) },
    },
  },
}));

import Home from "./Home";

describe("Home success interaction", () => {
  const scrollIntoView = vi.fn();

  beforeEach(() => {
    state.auth = { loading: false, isAuthenticated: true, error: null };
    state.mutation = { isPending: false, isSuccess: true, data: { diagnosticId: "diag-8", version: 8 } };
    Object.defineProperty(HTMLElement.prototype, "scrollIntoView", { configurable: true, value: scrollIntoView });
  });

  afterEach(() => {
    cleanup();
    scrollIntoView.mockReset();
  });

  it("scrolls to the diagnostic section after activating the successful-version action", () => {
    render(<Home />);
    fireEvent.click(screen.getByRole("button", { name: "Ver diagnóstico" }));
    expect(scrollIntoView).toHaveBeenCalledWith({ behavior: "smooth" });
  });
});
