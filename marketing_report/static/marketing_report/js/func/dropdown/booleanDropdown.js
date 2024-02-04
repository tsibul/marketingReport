'use strict'

/**
 * html code for boolean dropdown
 * @type {string}
 */
export const booleanDropdown = `<div class="dropdown report_dropdown dropdown_dict">
        <input name="bool" type="text" class="dropdown__hidden"
               value="1">
        <div class="dropdown__input-block">
            <input type="text" class="dropdown__input dropdown__input_dict"
                   placeholder="Поиск.."
                   value="Да"
                   data-value="Да" readonly>
            <i class="fa fa-solid fa-angle-down"></i>
        </div>
        <ul class="dropdown__content">
            <li data-value="1">Да</li>
            <li data-value="0">Нет</li>
        </ul>
    </div>
`;