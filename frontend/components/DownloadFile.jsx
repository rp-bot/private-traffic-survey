import { Entypo } from "@expo/vector-icons";
import React, { useState } from "react";
import {
	View,
	Text,
	Image,
	SafeAreaView,
	TouchableOpacity,
	Modal,
	Button,
} from "react-native";
import { firebase } from "../config";
import * as MediaLibrary from "expo-media-library";

const DownloadRecentImage = () => {
	const [imageUri, setImageUri] = useState(null);
	const [modalVisible, setModalVisible] = useState(false);

	const downloadMostRecentImage = async () => {
		try {
			const listRef = firebase.storage().ref("processed_images");
			const result = await listRef.listAll();
			if (result.items.length > 0) {
				const filesWithMetadata = await Promise.all(
					result.items.map(async (item) => ({
						fileRef: item,
						metadata: await item.getMetadata(),
					}))
				);
				filesWithMetadata.sort((a, b) =>
					b.metadata.timeCreated.localeCompare(a.metadata.timeCreated)
				);
				const recentFileRef = filesWithMetadata[0].fileRef;
				const url = await recentFileRef.getDownloadURL();
				setImageUri(url);
				setModalVisible(true);
			} else {
				Alert.alert("No images found in the directory.");
			}
		} catch (error) {
			console.error("Failed to fetch the images: ", error);
			Alert.alert("Failed to download the image.");
		}
	};

	const savePicture = async () => {
		if (imageUri) {
			try {
				const asset = await MediaLibrary.createAssetAsync(imageUri);
				alert("Picture saved! 🎉");
				setImage(null);
				console.log("saved successfully");
			} catch (error) {
				console.log(error);
			}
		}
		setModalVisible(false);
	};
	// const saveImage = async () => {
	// 	if (imageUri) {
	// 		const { status } = await MediaLibrary.requestPermissionsAsync();
	// 		if (status === "granted") {
	// 			await MediaLibrary.createAssetAsync(imageUri);
	// 			Alert.alert(
	// 				"Image Saved",
	// 				"The image has been saved to your photo gallery."
	// 			);
	// 		}
	// 	}
	// 	setModalVisible(false);
	// };

	const discardImage = () => {
		setModalVisible(false);
	};

	return (
		<SafeAreaView>
			<TouchableOpacity onPress={downloadMostRecentImage}>
				<Entypo name={"arrow-bold-down"} size={28} color={"#f1f1f1"} />
			</TouchableOpacity>
			<Modal
				animationType="slide"
				transparent={true}
				visible={modalVisible}
				onRequestClose={() => {
					Alert.alert("Modal has been closed.");
					setModalVisible(!modalVisible);
				}}
			>
				<View
					style={{
						flex: 1,
						justifyContent: "center",
						alignItems: "center",
						backgroundColor: "rgba(0, 0, 0, 0.5)",
					}}
				>
					<View
						style={{
							backgroundColor: "white",
							padding: 35,
							alignItems: "center",
							shadowColor: "#000",
							shadowOffset: { width: 0, height: 2 },
							shadowOpacity: 0.25,
							shadowRadius: 4,
							elevation: 5,
						}}
					>
						<Image
							source={{ uri: imageUri }}
							style={{ width: 300, height: 300 }}
						/>
						<Button title="Save to Device" onPress={savePicture} />
						<Button title="Discard" onPress={discardImage} />
					</View>
				</View>
			</Modal>
		</SafeAreaView>
	);
};

export default DownloadRecentImage;
