const add_option = (root, value, innerHTML, is_checked, checked_attribute) => {
    let opt = document.createElement('option');
    opt.value = value ? value : ""; 
    opt.innerHTML = innerHTML;
    
    if(is_checked){
        opt.setAttribute(checked_attribute,"");
    }

    root.appendChild(opt);
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('select[lazy_url]').forEach((e) =>{
        let rel_url = e.getAttribute('lazy_url');
        let value = e.getAttribute('data-value');
        let multiple_choice = e.getAttribute('data-allow-multiple-selected') != null;
        let checked_attribute = e.getAttribute('data-checked-attribute');
        
        let has_checked_an_option = false;

        fetch(rel_url)
            .then(data => data.json())
            .then(json => {
                if(!json.values){
                    throw "No 'values' key found in response"
                } else {
                    json.values.forEach(v => {
                        let is_checked = (multiple_choice && JSON.parse(v[0]).includes(value)) ||
                            (v[0] === value)
                        add_option(e, v[0],v[1], is_checked, checked_attribute);
                        
                        if(is_checked){
                            has_checked_an_option = true;
                        }
                    });
                }
            })
            .catch(err => {
                console.error(err);
            })
        
        if(!has_checked_an_option){
            add_option(e, null, "---------", true, checked_attribute)
        }
    })
})
