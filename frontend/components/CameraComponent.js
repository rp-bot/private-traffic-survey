import { Camera, CameraType } from 'expo-camera';
import { useState } from 'react';
import { Text, View, TouchableOpacity } from 'react-native';
import { TailwindProvider } from 'nativewind'; // Ensure you import TailwindProvider

export default function App() {
  const [type, setType] = useState(CameraType.back);
  const [permission, requestPermission] = Camera.useCameraPermissions();

  if (!permission) {
    // Camera permissions are still loading
    return <View />;
  }

  if (!permission.granted) {
    // Camera permissions are not granted yet
    return (
      <TailwindProvider>
        <View className="flex-1 justify-center items-center px-4">
          <Text className="text-center text-lg">We need your permission to show the camera</Text>
          <TouchableOpacity
            onPress={requestPermission}
            className="mt-4 bg-blue-500 rounded-lg p-2"
          >
            <Text className="text-white text-lg">Grant Permission</Text>
          </TouchableOpacity>
        </View>
      </TailwindProvider>
    );
  }

  function toggleCameraType() {
    setType(current => (current === CameraType.back ? CameraType.front : CameraType.back));
  }

  return (
    <TailwindProvider>
      <View className="flex-1 justify-center">
        <Camera className="flex-1" type={type}>
          <View className="flex-1 flex-row bg-transparent m-16 justify-center">
            <TouchableOpacity
              onPress={toggleCameraType}
              className="self-end pb-4"
            >
              <Text className="text-2xl font-bold text-white">Flip Camera</Text>
            </TouchableOpacity>
          </View>
        </Camera>
      </View>
    </TailwindProvider>
  );
}
