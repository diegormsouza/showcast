'use strict';

(() => {

    const refresh = new util.Refresh();

    const container = document.querySelector('#container');
    const columns = document.querySelector('div.columns');

    let carousels = new Array();

    let numberOfFramesShown = 5;

    let parameters = (new URL(document.location)).searchParams;

    let cat = parameters.get('cat').split(' '); //searchParams turns '+' into ' '
    let type = parameters.get('type').split(' ');
    let area = parameters.get('area').split(' ');

    refresh.set(() => {
        for (let i = 0; i < cat.length; i++) createCarousels(i, cat.length)
            .then(() => {
                if (i == cat.length - 1) {

                    let carouselPosition = 'duo';
                    if (cat.length > 2)
                        carouselPosition = 'quartet';

                    carousels.forEach((carousel) => {
                        document.querySelector('#' + carousel.getCarouselId()).classList.add(carouselPosition);
                    })
                }
            });

    }, 300000); //refresh every 5 minutes

    async function createCarousels(i, length) { //Async on this level so that carousels can load in parallel

        let imagesPath = '/Output/' + cat[i] + '/' + type[i] + "_" + area[i] + '/';

        let imagesURLs = await util.findFileUrls(imagesPath, "all", true);
        let imagesURLsSelection = imagesURLs.slice(Math.max(imagesURLs.length - numberOfFramesShown, 0));

        let j;

        if (length > 2) {
            if (i < 2) j = 1;
            else j = 2;
        }
        else {
            if (i == 0) j = 1;
            else j = 2;
        }


        let carousel = new Carousel('#col-' + j, { controls: false }, false);
        carousel.fill(imagesURLsSelection);

        let caption = document.createElement('p');
        caption.innerHTML = cat[i] + ' / ' + type[i] + ' / ' + area[i];
        carousel.addCaption(caption);

        carousels.push(carousel);
    }

    //Check every 50ms for the construction of the first image of all the carousels,
    //and then check for the image of the last one to load
    //(we do it like this because onload starts too late when loading from cache),
    //and then signal to all the carousels to play simultaneously
    const intervalOuter = setInterval(function () {
        let activeImages = document.querySelectorAll('.carousel-item.active img');

        if (activeImages.length == cat.length) {

            clearInterval(intervalOuter);

            let lastActiveImage = activeImages[activeImages.length - 1];

            const intervalInner = setInterval(() => {

                if (lastActiveImage.naturalWidth != 0) {

                    clearInterval(intervalInner);

                    for (let i = 0; i < carousels.length; i++) {
                        carousels[i].play();
                    }
                }

            }, 50);
        }
    }, 50);

})();