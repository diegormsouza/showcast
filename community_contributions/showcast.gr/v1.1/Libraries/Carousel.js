class Carousel {
    constructor(wrapperSelector, options, showIndex = true) {

        //create an options object to give to bootstrap carousel jQuery constructor, check bootstrap documentation for details
        this.defaultOptions = { interval: 1500, pause: 'false', keyboard: true, ride: false, controls: true }
        //properties of options with common names to those of defaultOptions will replace the latter's values
        //defaultOptions now contains the options inserted from the parameter
        Object.assign(this.defaultOptions, options);
        //get the element in which the carousel and other related divs will be created by this class
        this._wrapper = document.querySelector(wrapperSelector);
        this.carouselId = (() => `crsl-${Array.from(document.querySelectorAll('.carousel')).length++ || 0}`)();

        //call the function that creates, appends and returns the carousel element and assign it to a variable
        this.carouselElem = this._create();
        if (showIndex) this.indexTag = document.querySelector('#' + this.carouselId + ' .pageTagOverlay');
        this.carouselCaption = document.querySelector('#' + this.carouselId + ' .carousel-caption');
        //get the element with .carousel-inner css class in which the .carousel-item elements will be created
        this.inner = this.carouselElem.querySelector(".carousel-inner");
        this.imgSources = [];

        //carousel commands can only be used on the jquery object(unfortunately) so we mask the use of it. See control functions at the bottom
        //since js does not have static properties we start the ones that are meant to be used only within the class with a _
        this._jqCarousel = $(`#${this.carouselElem.id}`);
        this._control = command => { this._jqCarousel.carousel(command); } //simple function that delegates control to the jQuery object
        //event listener on the bootstrap carousel object 
        //listens for slide event completion to update the index tag
        if (showIndex) this._jqCarousel.on('slid.bs.carousel', (event) => {
            this.indexTag.textContent = `${(event.to + 1) || 1}/${this.imgSources.length}`; //if no slide number has been set, set 1 as default
        });
        //initialize the carousel
        this._control(this.defaultOptions);

        //enable keyboard control manually if the options ask for it because bootstrap carousel needs
        //focus on the left right buttons to make the keyboard work
        if (this.defaultOptions.keyboard) this.captureKeyboard(true);

        //set state play or pause according to the 'ride' option (see bootstrap carousel docs)
        this.currentState = this.defaultOptions.ride ? 'play' : 'pause';
        //set default state of transition
        this.defaultOptions.ride ? this.quickTransition(false) : this.quickTransition(true);


    }

    _create() {
        //count all bootstrap carousels on the page, increase the number by one and create the new carousel id
        let carouselOuter = document.createElement('div');
        carouselOuter.className = 'carousel slide pt-2 pb-2 carousel-fade h-100 align-items-center';
        carouselOuter.id = this.carouselId;
        carouselOuter.insertAdjacentHTML('afterbegin', `
            <div id="${this.carouselId}-inner" class="carousel-inner h-100"></div>
            <div class="carousel-caption"></div>
            <div class="pageTagOverlay"></div>
        `);

        ////handle control button visibility
        if (this.defaultOptions.controls) {
            carouselOuter.insertAdjacentHTML('beforeend',
                `
                    <div id="${this.carouselId}-play-button" class="pause-cycle-button carousel-play-button paused">
                        <button type="button" class="btn btn-primary btn-customized">
                            <i class="fas fa-play"></i>
                        </button>
                    </div>
                    <a class="carousel-control-prev" href="#slideshow-controls" data-target="#${this.carouselId}"
                        role="button" data-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="text-dark sr-only">Previous</span>
                    </a>
                    <a class="carousel-control-next" href="#slideshow-controls" data-target="#${this.carouselId}"
                        role="button" data-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class=" text-dark sr-only">Next</span>
                    </a>
                `
            );

            const playButton = carouselOuter.querySelector(`#${this.carouselId}-play-button`);
            const playButtonIcon = playButton.querySelector('i');

            playButton.addEventListener('click', event => {
                if (event.currentTarget.classList.contains('paused')) {
                    this.play();
                    playButton.classList.remove('paused');
                    playButtonIcon.classList.replace('fa-play', 'fa-pause');
                }
                else {
                    this.pause();
                    playButton.classList.add('paused');
                    playButtonIcon.classList.replace('fa-pause', 'fa-play');
                }
            });
        }

        this._wrapper.appendChild(carouselOuter);
        return carouselOuter;
    }

    insertAdjacentHTML(position, text) //overload
    {
        this.carouselElem.insertAdjacentElement(position, text);
    }

    fill(sources) {
        this.clear();
        this.imgSources = [].concat(sources || []);
        if (!this.imgSources.length) return;
        let frag = document.createDocumentFragment();

        this.imgSources.forEach((src, index) => {
            let item = document.createElement('div');
            let img = document.createElement('img');
            img.src = src;
            img.classList = 'd-block mx-auto';
            item.className = 'carousel-item h-100 d-flex align-items-center';

            //check image orientation and add the appropriate class(see theme.css)
            img.addEventListener("load", () => { //generalize below
                // console.log(img.naturalHeight, img.naturalWidth);
                if (img.naturalHeight > img.naturalWidth) img.classList.add("w-100");
                else if (img.naturalHeight < img.naturalWidth) { img.classList.add("h-100"); }
                else img.classList.add("h-100");

                //---Needed so that wheelzoom_upd.js can get the real, not inflated dimensions
                // if (img.naturalHeight >= img.naturalWidth) img.classList.add("h-100");
                // else img.classList.add("w-100");
            });
            item.setAttribute('data-index', `${index}`);
            if (index == 0) item.classList.add('active');
            item.appendChild(img);
            frag.appendChild(item);
        });
        this.inner.appendChild(frag);
        this._jqCarousel.trigger('slid.bs.carousel');
        if (this.imgSources.length == 1) return this.imgSources[0];
    }

    addCaption(elem) {
        this.carouselCaption.appendChild(elem);
    }

    hide() {
        let wrapperStyle = this._wrapper.style;
        if (wrapperStyle.display != 'none' || wrapperStyle == 'undefined') wrapperStyle.display = 'none';
        this.captureKeyboard(false);
    }

    reveal() {
        let wrapperStyle = this._wrapper.style;
        if (wrapperStyle.display == 'none' || wrapperStyle == 'undefined') wrapperStyle.display = 'block';
        this.captureKeyboard(true);
    }

    clear() {
        const existingItems = this.inner.children;
        if (existingItems.length != 0) Array.from(existingItems).forEach(child => child.remove());
        this.imgSources = [];
    }

    //Each slide on creation gets a data-index attribute with incrementing numbers
    getCurrentIndex() {
        let activeElem = this.inner.querySelector(".carousel-item.active");
        if (activeElem)
            return parseInt(activeElem.getAttribute('data-index'));
        else //If the carousel hasn't loaded yet, return the most recent element (the first it would load)
            return this.getSize();
    }

    getSize() {
        return this.imgSources.length;
    }

    addAnnotations(annotations) {
        const table = document.createElement('table');
        table.className = 'table annotations text-white';
        const tableBody = document.createElement('tbody');
        const row = document.createElement('tr');
        table.appendChild(tableBody);
        tableBody.appendChild(row);

        for (let annot of annotations) {
            const col = document.createElement('td');
            col.style.backgroundColor = annot.color;
            col.textContent = annot.text;
            row.appendChild(col);
        }
        this.annotationElem.appendChild(table);
    }

    captureKeyboard(bool) {
        let handleKeyDown = (event) => {
            if (event.defaultPrevented) return; // Do nothing if event already handled by another part of code

            switch (event.key) {
                case "ArrowLeft":
                    this.prev();
                    break;
                case "ArrowRight":
                    this.next();
                    break;
                default:
                    return;
            }
            event.preventDefault(); // Consume the event so it doesn't get handled twice
        }
        if (bool) $(window).on(`keydown.${this.carouselId}`, handleKeyDown)
        else $(window).off(`keydown.${this.carouselId}`);
    }

    pause(time = 0) { //pause for time in milliseconds, 
        this._control('pause'); //default is zero which means pause forever
        this.currentState = 'pause';
        this.quickTransition(true);
        if (time)
            setTimeout(() => {
                this.play();
                this.currentState = 'play';
            }, time);
    }

    play() {
        this._control('cycle');
        this.currentState = 'play';
        this.quickTransition(false);
    }

    prev() { this._control('prev'); }

    next() { this._control('next'); }

    dispose() { this._control('dispose'); }

    onSlid(run) {
        this._jqCarousel.on('slid.bs.carousel', run);
    }

    onSlide(run) {
        this._jqCarousel.on('slide.bs.carousel', run);
    }

    changeInterval(interval) {
        this._jqCarousel.data()['bs.carousel']["_config"].interval = interval;
    }

    slideTo(index) {
        this._control(index);
        this.currentState === 'play' ? this.play() : this.pause();
    }

    quickTransition(bool) {
        let carouselClasses = this.carouselElem.classList;
        if (bool && !carouselClasses.contains('quick-transition')) carouselClasses.add('quick-transition');
        else if (!bool && carouselClasses.contains('quick-transition')) carouselClasses.remove('quick-transition');
    }

    getCarouselId() {
        return this.carouselId;
    }

}