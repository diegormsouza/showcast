'use strict';

(() => {
    /////////////////////////////////
    //DECLARATION / INITIALLIZATION//
    /////////////////////////////////

    //capture sidepanel buttons
    const showGridButton = document.querySelector('#show-grid-button');
    const showCarouselButton = document.querySelector('#show-carousel-button');

    //get the carousel speed slider value
    //    let carouselInterval = parseInt(document.querySelector('#carouselSpeedRange').value);
    const carousel = new Carousel('#meteo-carousel', {controls: false });
    const gridGallery = new GridGallery('#meteo-grid', carousel, showCarouselButton);
    const viewPanelCardBody = document.querySelector('#view-panel > .card-body');
    const errorElem = document.querySelector('#error');

    const imageNumberTextbox = document.querySelector('#imageNumber');
    const totalImageNumberLabel = document.querySelector('#totalImageNumber');

    const fullScreenButton = document.querySelector('#fullscreen-button');

    let alt_areas, area_text, alt_area_texts;
    let area = 'DWD_Maps';
    let imagesPath;
    let activeImage;
    let container, containerDimensions, imageDimensions;
    let wheelZoom;
    //declare an array where we keep the image sources of each "set"
    let imagesURLs = [];
    let imagesURLsSelection = [];
    let previousImageNumber = 10;

    //view can take values 'carousel' or 'grid' and should be set only with the setView() function
    let view = "grid";

    let areas = ['DWD_Maps', 'DWD_Meteograms', 'ECMWF_Forecasts', 'UKMO_Maps'];
    let areas_texts = ['DWD Maps', 'DWD Meteograms', 'ECMWF Forecasts', 'UKMO Maps'];

    let activeImageContainer = {
        activeImage: null
    };
    let activeImageIndex = null;
    //    let gifWidth, gifWidthMin, gifHeight, gifHeightMin;
    const refresh = new util.Refresh();




    function setAreaParameters() { //Needs to be remade to use the 'areas' array / with function 'filter'?
        if (area === 'DWD_Maps') {
            alt_areas = ['DWD_Meteograms', 'ECMWF_Forecasts', 'UKMO_Maps'];
            area_text = 'DWD Maps';
            alt_area_texts = ['DWD Meteograms', 'ECMWF Forecasts', 'UKMO Maps'];
        } else if (area == 'DWD_Meteograms') {
            alt_areas = ['DWD_Maps', 'ECMWF_Forecasts', 'UKMO_Maps'];
            area_text = 'DWD Meteograms';
            alt_area_texts = ['DWD Maps', 'ECMWF Forecasts', 'UKMO Maps'];
        } else if (area == 'ECMWF_Forecasts') {
            alt_areas = ['DWD_Maps', 'DWD_Meteograms', 'UKMO_Maps'];
            area_text = 'ECMWF Forecasts';
            alt_area_texts = ['DWD Maps', 'DWD Meteograms', 'UKMO Maps'];
        } else if (area == 'UKMO_Maps') {
            alt_areas = ['DWD_Maps', 'DWD_Meteograms', 'ECMWF_Forecasts'];
            area_text = 'UKMO Maps';
            alt_area_texts = ['DWD Maps', 'DWD Meteograms', 'ECMWF Forecasts'];
        } else {
            console.error('Error: Unknown area');
        }

        imagesPath = '/Output/wmo_ra_vi/' + area + '/';
    }


    //Setup title, labels and switch buttons
    function insertParameters() {
        document.querySelector('title').innerHTML = "WMO RA VI";
        document.querySelector('.card-header').innerHTML += "<b>" + "WMO RA VI" + "</b> ";

        let areaButtons = [];
        for (let i = 0; i < areas.length; i++)
            areaButtons.push(util.createCategoryButton(areas[i], areas_texts[i]));

        // Δημιουργεί τα κουμπιά των φακέλων. Βάζω true, για να γίνουν κάθετα -vertical χρησιμοποιώντας τη util.js
        let groupBaseButtons = util.createGroupBaseButtons('base', areaButtons, clickedElem => {
            area = clickedElem;
            setAreaParameters();
            //There's a bug when switching between the grid of different areas, so we make sure that carousel loads first
            //showCarouselButton.click();
            setup();
        }, true);

        viewPanelCardBody.appendChild(groupBaseButtons);
    }

    //  Αλλάζει οπτική μεταξύ grid και carousel 
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

    //======== Uses getDirContents.php via util.js to return a list off addresses of the images in the given folder
    //  util.findFileUrls will fetch all files by setting "all" , or images by setting "image" ====================================================
    function fetchImages(dirUrl) {
        console.log("dirUrl: ");
        console.log(util.findFileUrls(dirUrl, "all", true));
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
            imagesURLsSelection = imagesURLs;
            setupCarouselAndGrid();
            container = document.querySelector('#meteo-carousel .carousel-item');
            containerDimensions = [container.offsetWidth, container.offsetHeight];
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
        container = document.querySelector('#meteo-carousel .carousel-item');
        let carouselImages = document.querySelectorAll('#meteo-carousel .carousel-item img');
//        let carouselImages = document.querySelectorAll('.carousel-item>img');
        activeImage = document.querySelector('#meteo-carousel .carousel-item.active img');

        activeImage.onload = () => {
            activeImage.onload = null;

            if (getDimensions) {
                imageDimensions = [activeImage.width, activeImage.height];
                containerDimensions = [container.offsetWidth, container.offsetHeight];
                console.log("imageDimensions:");   console.log(imageDimensions);    console.log(activeImage.src); 
                console.log("containerDimensions:");  console.log(containerDimensions);
            }

            wheelZoom = new Wheelzoom(carouselImages, activeImage, containerDimensions, imageDimensions, { zoom: 0.5 });

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

    document.querySelector('.btn-group .btn').click();


    setAreaParameters();
    insertParameters();

    document.querySelector('.area-btn .btn[area=DWD_Maps]').click(); //Click selected area button to setup the carousel

    //////////////////////////////////////////
    /////// SIDEPANEL FUNCTIONALITY //////////
    //////////////////////////////////////////

    // =================================== Grid Button button event listener ================================================
    showGridButton.addEventListener('click', event => {
        if (!showGridButton.classList.contains('active')) {
            setView('grid');
            showGridButton.classList.add("active");
            showCarouselButton.classList.remove("active");
        }
    })

    // ============================= Carousel Button button event listener ================================================
    showCarouselButton.addEventListener('click', event => {
        if (!showCarouselButton.classList.contains('active')) {
            setView('carousel');
            showCarouselButton.classList.add("active");
            showGridButton.classList.remove("active");
        }
    })


    // ====================================full screen button event listener ================================================
    fullScreenButton.addEventListener('click', event => {
        if ($(fullScreenButton).hasClass('active')) {
            util.closeFullscreen();
            fullScreenButton.classList.remove('active');
        } else {
            util.openFullscreen(document.body);
            fullScreenButton.classList.add('active');
        }
    })

    //=========================================carousel buttons event listeners ================================================
    document.querySelector('#carousel-play-button').addEventListener('click', event => {
        let crslPlayClasses = event.currentTarget.firstChild.classList;
        if (crslPlayClasses.contains('fa-pause')) {
            crslPlayClasses.replace('fa-pause', 'fa-play');
            event.currentTarget.classList.remove('active');
            carousel.pause();
        } else {
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


})()
