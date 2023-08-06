const add_option = (root, value, innerHTML, is_checked, checked_attribute) => {
    let opt = document.createElement('option');
    opt.value = value ? value : ""; 
    opt.innerHTML = innerHTML;
    
    if(is_checked){
        opt.setAttribute(checked_attribute,"");
    }

    root.appendChild(opt);
};

var finished_lazy_load = false;

document.addEventListener('DOMContentLoaded', () => {

    let url_to_elements = Array.prototype.reduce.call(document.querySelectorAll('select[lazy_url]'),
        ((acc,v) => {
            let rel_url = v.getAttribute('lazy_url');
            if(acc.get(rel_url)){
                acc.set(rel_url,[v,...acc.get(rel_url)])
                return acc;
            } else {
                acc.set(rel_url,[v]);
                return acc;
            }
        }),new Map());


    url_to_elements
    .forEach((es,rel_url) => {

        let json = fetch(rel_url)
        .then(data => data.json())

        es.forEach(e => {

            let form = e.closest("form");
            form.onsubmit = (event) => {
                event.preventDefault();
                if(finished_lazy_load){
                    form.submit()
                } else {
                    alert('Wait for the fields to load!')
                }
            }

            let value = e.getAttribute('data-value');
            let multiple_choice = e.getAttribute('data-allow-multiple-selected') != null;
            let checked_attribute = e.getAttribute('data-checked-attribute');

            let has_checked_an_option = false;

            json.then(json => {
                if (!json.values) {
                    throw "No 'values' key found in response";
                } else {
                    json.values.forEach(v => {
                        let is_checked = (multiple_choice && JSON.parse(v[0]).includes(value)) ||
                            (v[0] === value);
                        add_option(e, v[0], v[1], is_checked, checked_attribute);

                        if (is_checked) {
                            has_checked_an_option = true;
                        }
                    });
                }
            })
            .catch(err => {
                console.error(err);
            });
        })
    })

    finished_lazy_load = true;
})
