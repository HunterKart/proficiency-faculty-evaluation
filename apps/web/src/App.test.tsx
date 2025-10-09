import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import App from "./App";

const queryClient = new QueryClient();

vi.mock("./services/healthService", () => ({
  getHealth: () => Promise.resolve({ status: "ok" })
}));

describe("App", () => {
  it("renders the health status from the API", async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    );

    await waitFor(() =>
      expect(screen.getByText(/API status:/i)).toBeInTheDocument()
    );
  });
});
