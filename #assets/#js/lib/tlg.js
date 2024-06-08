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
		try {
			return fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrf,
				},
				body: JSON.stringify(msg),
			})
				.then(response => response.json())
		} catch (e) {
			console.error('sendData exeption:', e);
			return Promise.reject({
				status: 'error',
			});
		}
	},
	sendPhoto(photo, csrf) {
		try {
			const formData = new FormData();
			formData.append('file', photo);

			return fetch('/api/sendPhoto', {
				method: 'POST',
				headers: {
					'X-CSRFToken': csrf,
				},
				body: formData,
			})
				.catch(e => {
					console.error('sendPhoto exeption1:', e);
					return {
						status: 'error',
					};
				});
		} catch (e) {
			console.error('sendPhoto exeption2:', e);
			return Promise.reject({
				status: 'error',
			});
		}
	},
	sendPhotos(photos, csrf) {
		try {
			const formData = new FormData();
			photos.forEach(img => {
				formData.append('files', img);
			});

			return fetch('/api/sendPhotos', {
				method: 'POST',
				headers: {
					'X-CSRFToken': csrf,
				},
				body: formData,
			})
				.catch(e => {
					console.error('sendPhotos exeption1:', e);
					return {
						status: 'error',
					};
				});
		} catch (e) {
			console.error('sendPhotos exeption2:', e);
			return Promise.reject({
				status: 'error',
			});
		}
	},
};
