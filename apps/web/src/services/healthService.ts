import { healthResponseSchema, type HealthResponse } from "@proficiency/shared-types";

import { config } from "../lib/config";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${config.apiBaseUrl}/health`);

  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`);
  }

  const payload = await response.json();

  return healthResponseSchema.parse(payload);
}
