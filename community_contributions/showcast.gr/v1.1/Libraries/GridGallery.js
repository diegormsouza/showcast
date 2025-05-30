/*********************************************** DOCUMENTATION *********************************

Arguments : 
    - a selector for the element in which the GridGallery element will be created
    - an object of bootstrap carousel options(https://getbootstrap.com/docs/4.4/components/carousel/)

This class creates and manages an element containing a grid of image thumbnails each of which, when clicked,
opens a bootstrap modal. The modal contains a carousel which cycles starting from the image clicked. 

***********************************************************************************************/

class GridGallery {
    constructor(gridSelector, correspondingCarousel, carouselButton) {
        this.grid = document.querySelector(gridSelector);
        this.correspondingCarousel = correspondingCarousel;
        this.carouselButton = carouselButton;
        this.grid.className = 'h-100 pt-2 pb-2 d-flex flex-column align-self-center overflow-auto';
        this.hidden = true;
    }

    // urls as argument
    // creates array of img elements that act as thumbnails
    // A click event listener is attached to each element to go to the corresponding image in the carousel
    createThumbnails(sources) {
        let thumbs = [];
        let index = 0;
        for (let src of sources) {
            let thumb = document.createElement('img');
            thumb.src = src;
            thumb.setAttribute('data-grid-index', `${index}`);
            thumb.className = 'img-thumbnail img-fluid';
            thumb.addEventListener('click', () => {
                //start modal carousel from clicked image forward
                this.correspondingCarousel.slideTo(parseInt(thumb.getAttribute('data-grid-index')));
                this.carouselButton.click();
            })
            thumbs.push(thumb);
            index++;
        }
        return thumbs;
    }

    //urls as arguments. empty the grid and refill it with new. also fill the carousel with the same images.
    fill(images) {
        const thumbs = this.createThumbnails(images);
        if (this.grid.children.length) this.grid.querySelector('.row').remove(); //remove contents of the grid and recreate it with the new items
        this.createGrid(thumbs);
    }

    //create the grid and append thumbnails. argument is an array of img elements created by createThumbnails()
    createGrid(thumbs) {
        const row = document.createElement('div');
        row.className = 'row justify-content-center';
        for (let item of thumbs) {
            let column = document.createElement('div');
            column.className = `col-md-6 col-lg-4 col-6`;
            let imgWrapper = document.createElement('a');
            imgWrapper.className = 'd-block h-100 pt-2'
            imgWrapper.appendChild(item);
            column.appendChild(imgWrapper);
            row.appendChild(column);
            let column2 = column;
            row.appendChild(column2);
        }
        this.grid.appendChild(row);
        return row;
    }

    reveal() {
        if (this.grid.classList.contains('d-none')) {
            this.grid.classList.add('d-flex'); this.hidden = false;
            this.grid.classList.remove('d-none');
            this.hidden = false;
        }
    }
    hide() {
        if (!this.grid.classList.contains('d-none')) {
            this.grid.classList.add('d-none'); this.hidden = false;
            this.grid.classList.remove('d-flex');
            this.hidden = true;
        }
    }
}

