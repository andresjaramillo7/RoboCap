import React, { useMemo, useState } from "react";
import { Alert, Image, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import Header from "../components/Header";
import Button from "../components/Button";
import { pickFromGallery, takePhoto } from "../library/image";
import { uploadImageAndGetCaption } from "../library/api";

export default function App() {
    const [imageUri, setImageUri] = useState<string | null>(null);
    const [caption, setCaption] = useState<string>("");
    const [loading, setLoading] = useState(false);
    
    const captionReady = !!caption && !!imageUri;
    const hasImage = useMemo(() => !!imageUri, [imageUri]);

    async function onTakePhoto() {
        const r = await takePhoto();
        if (!r.ok) {
            if (r.reason === "denied") {
                Alert.alert("Permission needed", "Please allow camera access in Settings.");
            }
            return;
        }
        console.log("image camera uri:", r.uri);
        setImageUri(r.uri);
        setCaption("")
    }

    async function onPickGallery() {
        const r = await pickFromGallery();
        if (!r.ok) {
            if (r.reason === "denied") {
                Alert.alert("Permission needed", "Please allow photo library access in Settings.");
            }
            return;
        }
        console.log("image gallery uri:", r.uri);
        setImageUri(r.uri);
        setCaption("")
        }

    async function onGenerateCaption() {
        if (!imageUri) return;

        setLoading(true);
        setCaption("")
        console.log("[API] uploading:", imageUri);

        try {
            const cap = await uploadImageAndGetCaption(imageUri);
            console.log("api caption:", cap);

            setCaption(cap);
        } catch(e: any) {
            console.log("api error:", e?.message ?? e);
        } finally {
            setLoading(false)
        }
    }

    return (
        <SafeAreaView edges={["top", "bottom"]} className="flex-1 bg-black">
            <View className="flex-1 px-5 pt-4 pb-5 gap-5">
                <Header
                    title="RoboCap"
                    subtitle="Take a photo or pick one from your library. RoboCap will generate a caption."
                />

                <View className="flex-row gap-3">
                    <View className="flex-1">
                        <Button label="Take photo" onPress={onTakePhoto} iconName="camera" />
                    </View>
                    <View className="flex-1">
                        <Button
                            label="Gallery"
                            onPress={onPickGallery}
                            variant="secondary"
                            iconName="images"
                        />
                    </View>
                </View>

                <View className="flex-1 rounded-3xl overflow-hidden bg-zinc-900 border border-zinc-800">
                    {imageUri ? (
                        <Image source={{ uri: imageUri }} style={{ flex: 1 }} resizeMode="cover" />
                    ) : (
                        <View className="flex-1 items-center justify-center px-7 gap-3">
                            <View className="w-14 h-14 rounded-2xl bg-zinc-800 items-center justify-center">
                                <Ionicons name="image-outline" size={26} color="white" />
                            </View>
                            <Text className="text-white text-lg font-semibold text-center">
                                Add a photo to get started
                            </Text>
                            <Text className="text-zinc-400 text-center">
                                Choose Camera or Gallery, then generate a caption.
                            </Text>
                        </View>
                    )}
                </View>

                {hasImage && (
                    <>
                        <Button
                            label={loading ? "Generating..." : captionReady ? "Caption generated" : "Generate caption"}
                            onPress={onGenerateCaption}
                            disabled={!imageUri || loading}
                            variant={captionReady ? "success" : "primary"}
                            iconName={captionReady ? "checkmark-circle" : "sparkles"}
                        />

                        <View className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4">
                            <Text className="text-zinc-400 font-semibold">Caption</Text>
                            <Text className="text-white mt-2 leading-6">
                                {captionReady ? caption : loading ? "Working..." : "— Tap “Generate caption” to see the result."}
                            </Text>
                        </View>
                    </>
                )}
            </View>
        </SafeAreaView>
    );
}