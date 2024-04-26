import React, { useState, useEffect, useRef } from "react";
import { Text, View, StyleSheet, TouchableOpacity, Image } from "react-native";
import Constants from "expo-constants";
import { Camera, CameraType } from "expo-camera";
import * as MediaLibrary from "expo-media-library";
import { MaterialIcons } from "@expo/vector-icons";
import Button from "./components/Button";
import UploadMedia from "./components/UploadMedia";
import DownloadRecentImage from "./components/DownloadFile";
import { firebase } from "./config";
export default function App() {
	const [hasCameraPermission, setHasCameraPermission] = useState(null);
	const [image, setImage] = useState(null);
	const [type, setType] = useState(Camera.Constants.Type.back);
	const [flash, setFlash] = useState(Camera.Constants.FlashMode.off);
	const [uploading, setUploading] = useState(false);
	const cameraRef = useRef(null);

	useEffect(() => {
		(async () => {
			MediaLibrary.requestPermissionsAsync();
			const cameraStatus = await Camera.requestCameraPermissionsAsync();
			setHasCameraPermission(cameraStatus.status === "granted");
		})();
	}, []);

	const takePicture = async () => {
		if (cameraRef) {
			try {
				const data = await cameraRef.current.takePictureAsync();
				console.log(data);
				setImage(data.uri);
			} catch (error) {
				console.log(error);
			}
		}
	};
	const uploadClickedPic = async () => {
		if (image) {
			try {
				setUploading(true); // Assuming you have a state to track uploading status

				// First, create a blob from the image URI
				const blob = await new Promise((resolve, reject) => {
					const xhr = new XMLHttpRequest();
					xhr.onload = () => {
						resolve(xhr.response);
					};
					xhr.onerror = (e) => {
						reject(new TypeError("Network request failed"));
					};
					xhr.responseType = "blob";
					xhr.open("GET", image, true);
					xhr.send(null);
				});

				// Generate a filename based on the image URI
				const filename = image.substring(image.lastIndexOf("/") + 1);
				const ref = firebase
					.storage()
					.ref()
					.child("new_images")
					.child(filename);

				// Upload the blob to Firebase Storage
				await ref.put(blob);
				blob.close(); // Free up memory after upload

				// After a successful upload, save the image to the device's photo library
				// const asset = await MediaLibrary.createAssetAsync(image);
				alert("Picture saved and uploaded! 🎉");
				console.log("Saved and uploaded successfully");

				// Clear the image from state and stop uploading
				setImage(null);
				setUploading(false);
			} catch (error) {
				console.error(error);
				setUploading(false); // Ensure uploading is set to false in case of an error
				alert("Failed to save and upload the picture.");
			}
		}
	};

	const savePicture = async () => {
		if (image) {
			try {
				const asset = await MediaLibrary.createAssetAsync(image);
				alert("Picture saved! 🎉");
				setImage(null);
				console.log("saved successfully");
			} catch (error) {
				console.log(error);
			}
		}
	};

	if (hasCameraPermission === false) {
		return <Text>No access to camera</Text>;
	}

	return (
		<View style={styles.container}>
			{!image ? (
				<Camera
					style={styles.camera}
					type={type}
					ref={cameraRef}
					flashMode={flash}
				>
					<View
						style={{
							flexDirection: "row",
							justifyContent: "space-between",
							paddingHorizontal: 30,
						}}
					>
						<Button
							title=""
							icon="retweet"
							onPress={() => {
								setType(
									type === CameraType.back
										? CameraType.front
										: CameraType.back
								);
							}}
						/>
						<Button
							onPress={() =>
								setFlash(
									flash === Camera.Constants.FlashMode.off
										? Camera.Constants.FlashMode.on
										: Camera.Constants.FlashMode.off
								)
							}
							icon="flash"
							color={
								flash === Camera.Constants.FlashMode.off
									? "gray"
									: "#fff"
							}
						/>
					</View>
				</Camera>
			) : (
				<Image source={{ uri: image }} style={styles.camera} />
			)}

			<View style={styles.controls}>
				{image ? (
					<View
						style={{
							flexDirection: "row",
							justifyContent: "space-between",
							paddingHorizontal: 50,
						}}
					>
						<Button
							title="Discard"
							onPress={() => setImage(null)}
							icon="cross"
						/>
						<Button
							title="Upload"
							onPress={uploadClickedPic}
							icon="arrow-up"
						/>
					</View>
				) : (
					<View className="flex-col w-full">
						<View className="flex-row justify-between">
							<UploadMedia icon="image" />
							<DownloadRecentImage />
						</View>
						<View className="">
							<Button
								title="Take a picture"
								onPress={takePicture}
								icon="camera"
							/>
						</View>
					</View>
				)}
			</View>
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: "center",
		paddingTop: Constants.statusBarHeight,
		backgroundColor: "#000",
		padding: 8,
	},
	controls: {
		flex: 0.5,
	},
	button: {
		height: 40,
		borderRadius: 6,
		flexDirection: "row",
		alignItems: "center",
		justifyContent: "center",
	},
	text: {
		fontWeight: "bold",
		fontSize: 16,
		color: "#E9730F",
		marginLeft: 10,
	},
	camera: {
		flex: 5,
		borderRadius: 20,
	},
	topControls: {
		flex: 1,
	},
});
