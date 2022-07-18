grummer.tlg = {
	init() {},

	sendCallback(msg, csrf) {
		return this.sendData(msg, csrf, '/api/sendCallback');
	},

	sendFeedback(msg, csrf) {
		return this.sendData(msg, csrf, '/api/sendFeedback');
	},

	sendServices(msg, csrf) {
		return this.sendData(msg, csrf, '/api/sendServices');
	},

	sendData(msg, csrf, url) {
		return fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf,
			},
			body: JSON.stringify(msg),
		})
			.then(response => response.json())
			.then(json => {
				if (json.status !== 'success') throw json;
				return json;
			})
			.catch(e => {
				console.log('sendCallback exeption:', e);
				return {
					status: 'error',
				};
			});
	},

	sendMessage(msg, csrf) {
		return _asyncToGenerator(function* () {
			return yield fetch(API_URL_SEND_MESSAGE, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrf,
				},
				body: JSON.stringify(msg),
			})
				.then(response => response.json())
				.then(json => {
					if (json.status !== 'success') throw json;
					return json;
				})
				.catch(e => {
					console.log('sendMessage exeption:', e);
					return {
						status: 'error',
					};
				});
		})();
	},

	sendPhoto(photo, csrf) {
		return _asyncToGenerator(function* () {
			var formData = new FormData();
			formData.append('file', photo);
			return yield fetch(API_URL_SEND_PHOTO, {
				method: 'POST',
				headers: {
					// 'Content-Type': 'multipart/form-data',
					'X-CSRFToken': csrf,
				},
				body: formData,
			})
				.then(json => {
					if (json.status !== 'success') throw json;
					return json;
				})
				.catch(e => {
					console.log('sendPhoto exeption:', e);
					return {
						status: 'error',
					};
				});
		})();
	},

	sendPhotos(photos, csrf) {
		return _asyncToGenerator(function* () {
			var formData = new FormData();
			photos.forEach(img => {
				formData.append('files', img);
			});
			return yield fetch(API_URL_SEND_PHOTOS, {
				method: 'POST',
				headers: {
					// 'Content-Type': 'multipart/form-data',
					'X-CSRFToken': csrf,
				},
				body: formData,
			})
				.then(json => {
					if (json.status !== 'success') throw json;
					return json;
				})
				.catch(e => {
					console.log('sendPhotos exeption:', e);
					return {
						status: 'error',
					};
				});
		})();
	},
};
