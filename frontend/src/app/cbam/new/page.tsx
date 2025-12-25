import { redirect } from "next/navigation";

import { createCbamDeclaration, listCbamDeclarations } from "@/lib/api";
import type { CbamItemPayload } from "@/lib/types";

async function createSample() {
  const payload = {
    period: "2025-Q4",
    items: [
      {
        cn_code: "7208",
        product_description: "Flat-rolled steel",
        quantity_tonnes: 10,
        supplier_name: "Supplier A",
      },
      {
        cn_code: "7601",
        product_description: "Aluminum",
        quantity_tonnes: 5,
        verified_emission_factor: 10,
      },
    ] satisfies CbamItemPayload[],
  };
  await createCbamDeclaration(payload);
}

export default async function NewCbamPage() {
  await createSample();
  const list = await listCbamDeclarations();
  const newest = list[0];
  redirect("/cbam");
}
