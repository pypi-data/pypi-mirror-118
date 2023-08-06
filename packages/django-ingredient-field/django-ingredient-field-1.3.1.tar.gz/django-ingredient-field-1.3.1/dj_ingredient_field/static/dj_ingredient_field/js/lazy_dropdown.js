

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('select[lazy_url]').forEach((e) =>{
        let rel_url = e.getAttribute('lazy_url');
        let value = e.getAttribute('data-value');
        let multiple_choice = e.getAttribute('data-allow-multiple-selected') != null;
        let checked_attribute = e.getAttribute('data-checked-attribute');
        
        fetch(rel_url)
            .then(data => data.json())
            .then(json => {
                if(!json.values){
                    throw "No 'values' key found in response"
                } else {
                    json.values.forEach(v => {
                        let opt = document.createElement('option');
                        opt.value = v[0]; 
                        opt.innerHTML = v[1];
                        if ((multiple_choice && JSON.parse(v[0]).includes(value)) ||
                            (v[0] === value)){
                            opt.setAttribute(checked_attribute,checked_attribute);
                        }
                        e.appendChild(opt);
                    });
                }
            })
            .catch(err => {
                console.error(err);
            })
    })
})
