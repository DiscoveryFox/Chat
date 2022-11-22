import Sidebar from "./Sidebar";

const person1 = new Sidebar.ContactClass('Flinn', 2)
const person2 = new Sidebar.ContactClass('Alex', 1)
const contacts = [person1, person2]
function Chatwindow() {
    return (
        <div style={{ height: '100vh'}}>
            {Sidebar.Sidebar(contacts)}
        </div>
    )
}

export default Chatwindow