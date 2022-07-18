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
				.then(json => {
					if (json.status !== 'success') throw json;
					return json;
				});
		} catch (e) {
			console.error('sendCallback exeption:', e);
			return {
				status: 'error',
			};
		}
	},
	sendPhoto(photo, csrf) {
		const formData = new FormData();
		formData.append('file', photo);

		try {
			return fetch('/api/sendPhoto', {
				method: 'POST',
				headers: {
					'X-CSRFToken': csrf,
				},
				body: formData,
			}).then(json => {
				if (json.status !== 'success') throw json;
				return json;
			});
		} catch (e) {
			console.error('sendPhoto exeption:', e);
			return {
				status: 'error',
			};
		}
	},
	sendPhotos(photos, csrf) {
		const formData = new FormData();
		photos.forEach(img => {
			formData.append('files', img);
		});
		try {
			return fetch('/api/sendPhotos', {
				method: 'POST',
				headers: {
					'X-CSRFToken': csrf,
				},
				body: formData,
			}).then(json => {
				if (json.status !== 'success') throw json;
				return json;
			});
		} catch (e) {
			console.error('sendPhotos exeption:', e);
			return {
				status: 'error',
			};
		}
	},
};
