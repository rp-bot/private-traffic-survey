import {
	View,
	Text,
	TouchableOpacity,
	SafeAreaView,
	Alert,
	Image,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { firebase } from "../config";
import React, { useState } from "react";
import * as FileSystem from "expo-file-system";
import { Entypo } from "@expo/vector-icons";

export default UploadMedia = ({icon}) => {
	const [image, setImage] = useState(null);
	const [uploading, setUploading] = useState(false);

	const pickImages = async () => {
		let result = await ImagePicker.launchImageLibraryAsync({
			mediaTypes: ImagePicker.MediaTypeOptions.All,
			allowEditing: true,
			aspect: [4, 3],
			quality: 1,
		});

		if (!result.canceled) {
			setImage(result.assets[0].uri);
		}

		const uploadMedia = async () => {
			setUploading(true);
		};

		try {
			const { uri } = await FileSystem.getInfoAsync(image);
			const blob = await new Promise((resolve, reject) => {
				const xhr = new XMLHttpRequest();
				xhr.onload = () => {
					resolve(xhr.response);
				};
				xhr.onerror = (e) => {
					reject(new TypeError("Network request failed"));
				};
				xhr.responseType = "blob";
				xhr.open("GET", uri, true);
				xhr.send(null);
			});

			const filename = image.substring(image.lastIndexOf("/") + 1);
			const ref = firebase.storage().ref().child('new_images').child(filename); // Using .child() for clear path definition

            const snapshot = await ref.put(blob);
            blob.close(); // Free up memory
			setUploading(false);
			Alert.alert("Photo Uploaded!!");
			setImage(null);
		} catch (error) {
			console.error(error);
			setUploading(false);
		}
	};

	return (
		<SafeAreaView>
			<TouchableOpacity onPress={pickImages}>
				<Entypo name={icon} size={28} color={"#f1f1f1"} />
			</TouchableOpacity>
		</SafeAreaView>
	);
};
