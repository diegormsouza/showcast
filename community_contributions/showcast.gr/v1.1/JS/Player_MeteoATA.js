'use strict';

(() => {
    /////////////////////////////////
    //DECLARATION / INITIALLIZATION//
    /////////////////////////////////

    //capture sidepanel buttons
    const showGridButton = document.querySelector('#show-grid-button');
    const showCarouselButton = document.querySelector('#show-carousel-button');
    const createGifButton = document.querySelector('#create-gif-button');

    //get the carousel speed slider value
    let carouselInterval = parseInt(document.querySelector('#carouselSpeedRange').value);
    const carousel = new Carousel('#meteo-carousel', { interval: carouselInterval, controls: false });
    const gridGallery = new GridGallery('#meteo-grid', carousel, showCarouselButton);
    const viewPanelCardBody = document.querySelector('#view-panel > .card-body');
    const errorElem = document.querySelector('#error');

    const imageNumberTextbox = document.querySelector('#imageNumber');
    const totalImageNumberLabel = document.querySelector('#totalImageNumber');

    const fullScreenButton = document.querySelector('#fullscreen-button');

    const gifDimensionsRange = document.querySelector("#gifDimensionsRange");
    const gifDimensionsValue = document.querySelector("#gifDimensionsValue");
    const gifDimensionsLabel = document.querySelector("#gifDimensionsLabel");

    let cat, type, area, alt_areas, area_text, alt_area_texts, full_name = 'ShowCast', alt_full_name;
    let parsedParameters;
    let imagesPath;

    let containerDimensions, imageDimensions;

    let wheelZoom;
    //declare an array where we keep the image sources of each "set"
    let imagesURLs = [];
    let imagesURLsSelection = [];
    let previousImageNumber = 10;

    //view can take values 'carousel' or 'grid' and should be set only with the setView() function
    let view = "carousel";

    let areas = ['FDK', 'EU', 'GR'];
    let areas_texts = ['FDK', 'EUR', 'GRC'];

    let activeImageContainer = { activeImage: null };
    let activeImageIndex = null;
    let gifWidth, gifWidthMin, gifHeight, gifHeightMin;
    const refresh = new util.Refresh();

    function getParameters() {
        let parameters = (new URL(document.location)).searchParams;

        //Get URL parameters
        cat = parameters.get('cat');
        type = parameters.get('type');
        area = parameters.get('area');
    }

    function setAreaParameters() {//Needs to be remade to use the 'areas' array / with function 'filter'?
        if (area === 'FDK') {
            alt_areas = ['EU', 'GR'];
            area_text = 'FDK';
            alt_area_texts = ['EUR', 'GRC'];
        }
        else if (area == 'EU') {
            alt_areas = ['FDK', 'GR'];
            area_text = 'EUR';
            alt_area_texts = ['FDK', 'GRC'];
        }
        else if (area == 'GR') {
            alt_areas = ['FDK', 'EU'];
            area_text = 'GRC';
            alt_area_texts = ['FDK', 'EUR'];
        }
        else {
            console.error('Error: Unknown area');
        }

        full_name = cat + '_' + type + '_' + area;

        imagesPath = '/Output/' + cat + '/' + type + "_" + area + '/';
        console.log(imagesPath);
    }


    //Setup title, labels and switch buttons
    function insertParameters() {
        document.querySelector('title').innerHTML = cat + ' ' + type;
        document.querySelector('.card-header').innerHTML += "<b>" + cat + "</b> " + type;

        let areaButtons = [];
        for (let i = 0; i < areas.length; i++)
            areaButtons.push(util.createCategoryButton(areas[i], areas_texts[i]));

        let groupBaseButtons = util.createGroupBaseButtons('base', areaButtons, clickedElem => {
            area = clickedElem;
            setAreaParameters();
            //There's a bug when switching between the grid of different areas, so we make sure that carousel loads first
            showCarouselButton.click();
            setup();
        });

        viewPanelCardBody.appendChild(groupBaseButtons);
    }


    function setView(newView) { //takes 'carousel', 'grid' or 'error' as arguments

        panelVisibility('all', true);

        switch (newView) {
            case 'carousel':
                view = 'carousel';
                let activeImageIndex = 0;
                let activeImage = document.querySelector('#meteo-carousel .carousel-item.active img');
                if (activeImage) {
                    let activeImageURL = activeImage.src;
                    activeImageIndex = imagesURLsSelection.findIndex(imageURL => activeImageURL == imageURL);
                }
                errorElem.style.display = 'none';
                gridGallery.hide();
                carousel.reveal();
                break;

            case 'grid':
                view = 'grid';
                carousel.hide();
                errorElem.style.display = 'none';
                gridGallery.reveal();

                let selectedGridElem = document.querySelector('img[data-grid-index="' + carousel.getCurrentIndex() + '"]');

                if (selectedGridElem !== null) //Focus on the element only if it has loaded yet
                {
                    selectedGridElem.focus();
                    selectedGridElem.scrollIntoView();
                }
                break;

            case 'error':
                errorElem.style.display = 'block';
                gridGallery.hide();
                carousel.hide();
                break;
        }
    }

    function fetchImages(dirUrl) {
        console.log("dirUrl: ");
        console.log(util.findFileUrls(dirUrl, "image", true));
        return util.findFileUrls(dirUrl, "image", true); //ideally should be 'image', but it checks the files one by one and significantly delays
    }

    function panelVisibility(panelName = 'side-panel', visib = true) {
        if (panelName === 'all') {
            const allPanels = Array.from(document.querySelectorAll("[id*='-panel']"));
            for (let panel of allPanels) {
                panelVisibility(panel.id, visib);
            }
            return;
        }
        let panel = document.querySelector(`#${panelName}`);
        if (!panel.classList.replace(visib ? 'd-none' : 'side-block', visib ? 'side-block' : 'd-none')) {
            visib ? panel.classList.add('side-block') : panel.classList.add('d-none');
        }
    }


    function setup() {
        refresh.set(async () => {
            imagesURLs = await fetchImages(imagesPath);
            // imagesURLs = imagesURLs.reverse();

            totalImageNumberLabel.value = imagesURLs.length;
            imageNumberTextbox.value = 10;

            if (imageNumberTextbox.value > totalImageNumberLabel.value)
                imageNumberTextbox.value = totalImageNumberLabel.value;
            // imagesURLsSelection = imagesURLs.slice(0, imageNumberTextbox.value);
            imagesURLsSelection = imagesURLs.slice(Math.max(imagesURLs.length - imageNumberTextbox.value, 0));

            //gif functionality
            gifDimensionsRange.value = 50;
            gifDimensionsValue.innerHTML = 50 + "%";
            gifDimensionsLabel.innerHTML = "GIF dimensions";
            let img = new Image();
            img.onload = function () {
                gifWidth = this.width;
                gifHeight = this.height;
                setGifDimensions();
            }
            img.src = imagesURLs[0];//pairnei tin proti eikona. tha prepei na parei tin teleytaia anoigontas

            setupCarouselAndGrid();

            //refetch and render newest images every 5 minutes
        }, 300000);
    }

    function setupCarouselAndGrid(getDimensions = true, slideIndex = imagesURLsSelection.length - 1) {
        carousel.fill(imagesURLsSelection);
        gridGallery.fill(imagesURLsSelection);
        !imagesURLsSelection.length ? setView("error") : setView(view);
        setupWheelzoom(getDimensions, slideIndex);
    }

    function setupWheelzoom(getDimensions = true, slideIndex) {

        let container = document.querySelector('#meteo-carousel .carousel-item');
        let carouselImages = document.querySelectorAll('#meteo-carousel .carousel-item img');
        let activeImage = document.querySelector('#meteo-carousel .carousel-item.active img');

        activeImage.onload = () => {
            activeImage.onload = null;

            if (getDimensions) {
                imageDimensions = [activeImage.width, activeImage.height];
                containerDimensions = [container.offsetWidth, container.offsetHeight];
            }

            wheelZoom = new Wheelzoom(carouselImages, activeImage, containerDimensions, imageDimensions, { zoom: 0.2 });

            carousel.onSlide((event) => {
                activeImage = document.querySelector('#meteo-carousel .carousel-item[data-index="' + event.to + '"] img');
                wheelZoom.setActiveImage(activeImage);
            });

            //When the loading of the carousel finishes, by default go to the most recent product
            carousel.slideTo(slideIndex);
        }
    }

    function resizeCarousel() {
        let currentIndex = carousel.getCurrentIndex();
        setupCarouselAndGrid(true, currentIndex);
    }


    ////////////////////////
    /// LOGIC //////////////
    ////////////////////////

    // document.querySelector('.btn-group .btn').click();

    getParameters();
    setAreaParameters();
    insertParameters();

    document.querySelector('.area-btn .btn[area=' + area + ']').click(); //Click selected area button to setup the carousel

    //////////////////////////////////////////
    /////// SIDEPANEL FUNCTIONALITY //////////
    //////////////////////////////////////////

    showGridButton.addEventListener('click', event => {
        if (!showGridButton.classList.contains('active')) {
            setView('grid');
            showGridButton.classList.add("active");
            showCarouselButton.classList.remove("active");
        }
    })

    showCarouselButton.addEventListener('click', event => {
        if (!showCarouselButton.classList.contains('active')) {
            setView('carousel');
            showCarouselButton.classList.add("active");
            showGridButton.classList.remove("active");
        }
    })

    document.querySelector('#carouselSpeedRange').addEventListener('change', event => {
        carouselInterval = parseInt(event.target.value);
        carousel.changeInterval(carouselInterval);
    })

    fullScreenButton.addEventListener('click', event => {
        if ($(fullScreenButton).hasClass('active')) {
            util.closeFullscreen();
            fullScreenButton.classList.remove('active');
        }
        else {
            util.openFullscreen(document.body);
            fullScreenButton.classList.add('active');
        }
    })

    document.querySelector('#carousel-play-button').addEventListener('click', event => {
        let crslPlayClasses = event.currentTarget.firstChild.classList;
        if (crslPlayClasses.contains('fa-pause')) {
            crslPlayClasses.replace('fa-pause', 'fa-play');
            event.currentTarget.classList.remove('active');
            carousel.pause();
        }
        else {
            crslPlayClasses.replace('fa-play', 'fa-pause');
            event.currentTarget.classList.add('active');
            carousel.play();
        }
    })
    document.querySelector('#carousel-prev-button').addEventListener('click', event => {
        carousel.prev();
    })
    document.querySelector('#carousel-next-button').addEventListener('click', event => {
        carousel.next();
    })

    $(totalImageNumber).click(() => {
        if (totalImageNumberLabel.value != imageNumberTextbox.value) {
            previousImageNumber = imageNumberTextbox.value;
            imageNumberTextbox.value = totalImageNumberLabel.value;
            imagesURLsSelection = imagesURLs;

            setupCarouselAndGrid();
        }
    });

    $(imageNumberTextbox).change(() => {
        let imgNum = parseInt(imageNumberTextbox.value);
        if (imgNum < 1)
            imgNum = 1;
        else if (imgNum > totalImageNumberLabel.value)
            imgNum = totalImageNumberLabel.value;
        else if (isNaN(imgNum))
            imgNum = previousImageNumber;

        imageNumberTextbox.value = imgNum;
        previousImageNumber = imgNum;

        imagesURLsSelection = imagesURLs.slice(Math.max(imagesURLs.length - imgNum, 0));

        setupCarouselAndGrid(false);
    });

    window.addEventListener('resize', resizeCarousel);

    $('[data-toggle="tooltip"]').tooltip();

    function setGifDimensions() {
        gifWidthMin = Math.round(gifWidth * gifDimensionsRange.value / 100);
        gifHeightMin = Math.round(gifHeight * gifDimensionsRange.value / 100);
        gifDimensionsValue.innerHTML = gifDimensionsRange.value + "%";
        gifDimensionsLabel.innerHTML = "GIF dimensions: " + gifWidthMin + " x " + gifHeightMin;
    }

    gifDimensionsRange.oninput = function () {
        setGifDimensions();
    }

    createGifButton.addEventListener('click', event => {

        //start the loading spinner
        createGifButton.firstElementChild.classList.replace('fa-download', 'fa-spinner');
        createGifButton.firstElementChild.classList.add('fa-spin');

        let frameDuration = carouselInterval / 100;

        gifshot.createGIF({
            'images': imagesURLsSelection, 'frameDuration': frameDuration, 'gifWidth': gifWidthMin, 'gifHeight': gifHeightMin
        }, function (obj) {
            if (!obj.error) {
                createGifButton.firstElementChild.classList.replace('fa-spinner', 'fa-download');
                createGifButton.firstElementChild.classList.remove('fa-spin');

                const a = document.createElement("a");
                a.href = obj.image;
                a.download = full_name;
                document.body.appendChild(a);
                a.click();
                a.remove();
            }
        });

    })
})()
