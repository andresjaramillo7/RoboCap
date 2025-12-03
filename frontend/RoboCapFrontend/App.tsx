import "./global.css";
import { SafeAreaProvider } from "react-native-safe-area-context";
import App from "./src/app/App";

export default function Root() {
    return (
        <SafeAreaProvider>
            <App />
        </SafeAreaProvider>
    );
}
