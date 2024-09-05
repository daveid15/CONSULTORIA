import "regenerator-runtime"
import {createItemFilter, getLabelAreas, setAllServicesElements} from "./utils";

let seeAllBtn = document.getElementById('item_all');

seeAllBtn.addEventListener('click', async (evt) => {
    let element = evt.target

    let itemActive = document.getElementById('filters-menu').querySelector('.active');

    if (itemActive !== null) {
        itemActive.classList.remove('active')
    }

    element.classList.add('active')

    await setAllServicesElements();
});

window.addEventListener('load', async () => {

    let filter_menu = document.getElementById('filters-menu');

    let areas = await getLabelAreas();

    areas.map((item) => {
        filter_menu.appendChild(createItemFilter(item.area_name, item.area_id))
    });

    filter_menu.children.item(0)

    await setAllServicesElements();

})