/*!
	Wheelzoom 4.0.1
	license: MIT
	http://www.jacklmoore.com/wheelzoom

	Modified to work on MeteoATA Bootstrap Carousel
	Has not been updated or tested to support initialZoom
*/

class Wheelzoom {

	//Assuming each image has the same dimensions, 
	//we'll make calculations on the active image and apply the same to the rest

	constructor(images, activeImage, containerDimensions, imageDimensions, options) {

		this.activeImage = activeImage;
		this.images = images;

		this.containerDimensions = containerDimensions;
		this.imageDimensions = imageDimensions;

		var defaults = {
			zoom: 0.10,
			maxZoom: false,
			initialZoom: 1,
			initialX: 0.5,
			initialY: 0.5,
		};

		this.orientationCentered = null;

		this.activeImage.addEventListener('wheelzoom.destroy', event => { this.destroy() });

		options = options || {};

		this.settings = {};

		for (let key in defaults) {
			this.settings[key] = options[key] !== undefined ? options[key] : defaults[key];
		}

		let handlerMousemove;
		let handlerFullvisible;
		let handlerMouseup;
		let handlerWheelzoomReset;
		let handlerLoad;
		let handlerMousedown;
		let handlerWheel;
		
		this.load();
	}

	load() {
		var initial = Math.max(this.settings['initialZoom'], 1);

		if (this.activeImage.src === this.transparentSpaceFiller) return;

		this.nWidth = this.activeImage.naturalWidth;
		this.nHeight = this.activeImage.naturalHeight;

		this.width = this.imageDimensions[0];
		this.height = this.imageDimensions[1];

		this.centeredPos = [];

		this.centeredPos[0] = (this.containerDimensions[0] / 2 - this.width / 2);
		this.centeredPos[1] = (this.containerDimensions[1] / 2 - this.height / 2);

		this.bgWidth = this.width * initial;
		this.bgHeight = this.height * initial;

		this.bgPosX = -(this.bgWidth - this.width) * this.settings.initialX;
		this.bgPosY = -(this.bgHeight - this.height) * this.settings.initialY;

		this.bgPosX += this.centeredPos[0];
		this.bgPosY += this.centeredPos[1];

		// console.log(this.width, this.height, this.nWidth, this.nHeight);

		this.setSrcToBackground();
		this.setActiveImage(this.activeImage, false);
	}

	setSrcToBackground() {
		for (let i = 0; i < this.images.length; i++) {
			this.images[i].style.backgroundRepeat = 'no-repeat';

			this.images[i].classList.add("w-100"); //Needed to make sure it works for all ratios
			this.images[i].classList.add("h-100");

			this.images[i].style.backgroundImage = 'url("' + this.images[i].src + '")';
			this.transparentSpaceFiller = 'data:image/svg+xml;base64,' + window.btoa('<svg xmlns="http://www.w3.org/2000/svg" this.width="' + this.activeImage.naturalWidth + '" this.height="' + this.activeImage.naturalHeight + '"></svg>');
			this.images[i].src = this.transparentSpaceFiller;
		}
	}

	setActiveImage(activeImage, isNew = true) {
		if (isNew) this.destroyActiveImageListeners();

		this.activeImage = activeImage;
		this.activeImage.style.backgroundSize = this.bgWidth + 'px ' + this.bgHeight + 'px';
		this.activeImage.style.backgroundPosition = this.bgPosX + 'px ' + this.bgPosY + 'px';
		this.activeImage.addEventListener('wheelzoom.reset', this.handlerWheelzoomReset = () => { this.reset() });

		this.activeImage.addEventListener('wheel', this.handlerWheel = (event) => { this.onwheel(event) });
		this.activeImage.addEventListener('mousedown', this.handlerMousedown = (event) => { this.draggable(event) });
	}

	updateBgStyle() {
		if (this.bgPosX > 0) {
			document.dispatchEvent(new Event('full-visible'));
		}

		this.activeImage.style.backgroundSize = this.bgWidth + 'px ' + this.bgHeight + 'px';
		this.activeImage.style.backgroundPosition = this.bgPosX + 'px ' + this.bgPosY + 'px';
	}

	reset() {
		this.bgWidth = this.width;
		this.bgHeight = this.height;
		
		this.bgPosX = this.centeredPos[0];
		this.bgPosY = this.centeredPos[1];	

		this.updateBgStyle();
	}

	onwheel(e) {
		var deltaY = 0;
		e.preventDefault();
		if (e.deltaY) { // FireFox 17+ (IE9+, Chrome 31+?)
			deltaY = e.deltaY;
		} else if (e.wheelDelta) {
			deltaY = -e.wheelDelta;
		}

		// As far as I know, there is no good cross-browser way to get the cursor position relative to the event target.
		// We have to calculate the target element's position relative to the document, and subtrack that from the
		// cursor's position relative to the document.
		var rect = this.activeImage.getBoundingClientRect();
		var offsetX = e.pageX - rect.left - window.pageXOffset;
		var offsetY = e.pageY - rect.top - window.pageYOffset;

		// Record the offset between the bg edge and cursor:
		var bgCursorX = offsetX - this.bgPosX;
		var bgCursorY = offsetY - this.bgPosY;

		// Use the previous offset to get the percent offset between the bg edge and cursor:
		var bgRatioX = bgCursorX / this.bgWidth;
		var bgRatioY = bgCursorY / this.bgHeight;

		// Update the bg size:
		if (deltaY < 0) {
			this.bgWidth += this.bgWidth * this.settings.zoom;
			this.bgHeight += this.bgHeight * this.settings.zoom;
		} else {
			this.bgWidth -= this.bgWidth * this.settings.zoom;
			this.bgHeight -= this.bgHeight * this.settings.zoom;
		}

		if (this.settings.maxZoom) {
			this.bgWidth = Math.min(this.width * this.settings.maxZoom, this.bgWidth);
			this.bgHeight = Math.min(this.height * this.settings.maxZoom, this.bgHeight);
		}

		// Take the percent offset and apply it to the new size:
		this.bgPosX = offsetX - (this.bgWidth * bgRatioX);
		this.bgPosY = offsetY - (this.bgHeight * bgRatioY);

		// Prevent zooming out beyond the starting size or dragging beyond the canvas
		//For now it doesn't work on the right
		if ((this.bgWidth <= this.width || this.bgHeight <= this.height) 
			|| ((this.bgWidth == this.width || this.bgHeight == this.height) && (this.bgPosY!=this.centeredPos || this.bgPosX!=this.centeredPos))) {
//			this.reset();   //εμποδίζει τη σμίκρυνση της εικόνας κάτω από το μέγεθός της.
            this.updateBgStyle(); // επιτρέπει την σμίκρυνση

		} else {
			this.updateBgStyle();
		}
	}

	drag(e) {
		e.preventDefault();
		this.bgPosX += (e.pageX - this.previousEvent.pageX);
		this.bgPosY += (e.pageY - this.previousEvent.pageY);
		this.previousEvent = e;
		this.updateBgStyle();
	}
	

	// Make the background draggable
	draggable(e) {
		e.preventDefault();
		this.previousEvent = e;
		document.addEventListener('mousemove', this.handlerMousemove = (event) => { this.drag(event) });
		document.addEventListener('full-visible', this.handlerFullvisible = () => { this.removeDrag() });
		document.addEventListener('mouseup', this.handlerMouseup = () => { this.removeDrag() });
	}

	removeDrag() {
		document.removeEventListener('mousemove', this.handlerMousemove);
		document.removeEventListener('full-visible', this.handlerFullvisible);
		document.removeEventListener('mouseup', this.handlerMouseup);
	}

	destroy(originalProperties) {
		this.destroyActiveImageListeners();

		this.activeImage.style.backgroundImage = originalProperties.backgroundImage;
		this.activeImage.style.backgroundRepeat = originalProperties.backgroundRepeat;
		this.activeImage.src = originalProperties.src;
	}

	destroyActiveImageListeners() {
		// console.log('destroy');
		this.activeImage.removeEventListener('wheelzoom.reset', this.handlerWheelzoomReset);
		this.activeImage.removeEventListener('load', this.handlerLoad);
		this.activeImage.removeEventListener('mouseup', this.handlerMouseup);
		this.activeImage.removeEventListener('mousemove', this.handlerMousemove);
		this.activeImage.removeEventListener('mousedown', this.handlerMousedown);
		this.activeImage.removeEventListener('wheel', this.handlerWheel);
	}
}
