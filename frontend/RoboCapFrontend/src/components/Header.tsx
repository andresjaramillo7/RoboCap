import { Text, View } from "react-native";

type Props = {
  title: string;
  subtitle: string;
};

export default function Header({ title, subtitle }: Props) {
  return (
    <View className="gap-2">
      <Text className="text-white text-3xl font-extrabold">{title}</Text>
      <Text className="text-zinc-400 text-base">{subtitle}</Text>
    </View>
  );
}