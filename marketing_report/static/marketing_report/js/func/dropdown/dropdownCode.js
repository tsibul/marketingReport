'use strict'

/**
 * html code for dropdown
 * @type {string}
 */
export const dropdownCode = `
    <div class="dropdown report_dropdown dropdown_dict">
        <input name="" type="text" class="dropdown__hidden"
               value="">
        <div class="dropdown__input-block">
            <input type="text" class="dropdown__input dropdown__input_dict"
                   placeholder="Поиск.." 
                   value=""
                   data-value="">
            <i class="fa fa-solid fa-angle-down"></i>
        </div>
        <ul class="dropdown__content">
        </ul>
    </div>
`;