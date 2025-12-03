import React from "react";
import { Pressable, Text } from "react-native";
import { Ionicons } from "@expo/vector-icons";

type Props = {
    label: string;
    onPress: () => void;
    variant?: "primary" | "secondary" | "success";
    disabled?: boolean;
    iconName?: React.ComponentProps<typeof Ionicons>["name"];
};

export default function Button({
    label,
    onPress,
    variant = "primary",
    disabled = false,
    iconName,
}: Props) {
    const base = "h-14 rounded-2xl px-4 flex-row items-center justify-center gap-2 border";

    const palette =
        variant === "primary"
            ? "bg-blue-600 border-blue-500"
            : variant === "success"
            ? "bg-emerald-600 border-emerald-500"
            : "bg-zinc-900 border-zinc-800";

    return (
        <Pressable
            onPress={onPress}
            disabled={disabled}
            accessibilityRole="button"
            android_ripple={{ color: "rgba(255,255,255,0.12)" }}
            style={({ pressed }) => [
                {
                    opacity: disabled ? 0.5 : pressed ? 0.85 : 1,
                    transform: [{ scale: pressed ? 0.98 : 1 }],
                },
            ]}
            className={`${base} ${palette}`}
        >
            {iconName ? <Ionicons name={iconName} size={18} color="white" /> : null}
            <Text className="text-white font-semibold">{label}</Text>
        </Pressable>
    );
}