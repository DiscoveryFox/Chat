import './Sidebar.css';

class ContactClass {
    name: string;
    id: number;

    public constructor(name: string, id: number) {
        this.id = id;
        this.name = name;
    }
}

function Contact(name: string, id: number) {
    return (
        <div className="contact-card" id={id.toString()} key={id.toString()}>
            <p>👤{name}</p>
        </div>
    )
}

function Sidebar(contacts: Array<ContactClass>) {
    return (
        <div className="sidebar">
            <div id="contact_searchbar_outer_div">
                <input type="text" id="contact_searchbar_inner_div" >

                </input>
            </div>
            {contacts.map(function (contact, i) {
                return Contact(contact.name, contact.id)
            })}
        </div>
    )
}

export default {Sidebar, ContactClass};