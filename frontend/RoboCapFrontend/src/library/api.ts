import { API_BASE_URL, CAPTION_PATH, IMAGE_FIELD_NAME } from "../config";

export async function uploadImageAndGetCaption(imageUri: string): Promise<string> {
    const url = `${API_BASE_URL}${CAPTION_PATH}`;
    console.log("[API] POST", url);

    const form = new FormData();
    form.append(
        IMAGE_FIELD_NAME,
        { uri: imageUri, name: "photo.jpg", type: "image/jpeg" } as any,
    );

    const res = await fetch(url, { method: "POST", body: form });

    if (!res.ok) {
        const text = await res.text().catch(() => "");
        console.log("[API] HTTP", res.status, text);
        throw new Error(`HTTP ${res.status}: ${text}`);
    }

    const data = await res.json();
    if (!data?.caption) throw new Error("Backend response missing `caption`.");
    return data.caption;
}