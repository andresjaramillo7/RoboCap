import * as ImagePicker from "expo-image-picker";

export type ImagePickResult =
    | { ok: true; uri: string }
    | { ok: false; reason: "denied" | "canceled" };

export async function pickFromGallery(): Promise<ImagePickResult> {
    const perm = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!perm.granted) return { ok: false, reason: "denied" };

    const result = await ImagePicker.launchImageLibraryAsync({
        quality: 0.85,
    });

    if (result.canceled) return { ok: false, reason: "canceled" };
    return { ok: true, uri: result.assets[0].uri };
}

export async function takePhoto(): Promise<ImagePickResult> {
    const perm = await ImagePicker.requestCameraPermissionsAsync();
    if (!perm.granted) return { ok: false, reason: "denied" };

    const result = await ImagePicker.launchCameraAsync({
        quality: 0.85,
    });

    if (result.canceled) return { ok: false, reason: "canceled" };
    return { ok: true, uri: result.assets[0].uri };
}