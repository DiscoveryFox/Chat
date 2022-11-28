import Sidebar from "./Sidebar";
import React from "react";
import './Chatwindow.css'
const person1 = new Sidebar.ContactClass('Flinn', 2)
const person2 = new Sidebar.ContactClass('Alex', 1)
const contacts = [person1, person2]

// TODO: Find out why there is a white border at the top of the react page.

class ClassicMessage {
    from: string;
    to: string;
    text: string;
    timestamp: string;

    public constructor(from: string, to: string, text: string, timestamp: string) {
        this.from = from;
        this.to = to;
        this.text = text;
        this.timestamp = timestamp
    }
}

function gen_key_from_ClassicMessage(message: ClassicMessage) {
    return message.from + message.to + message.timestamp
}

function fetch_username_from_api() {
    // find out why this fetch doesn't load and make it, so it works properly
    //fetch('http://127.0.0.1:5000/get_my_username', {headers: {'Request-Mode': 'no-cors', 'Access-Control-Allow-Origin': 'no-cors'} }).then(r => {
    //    console.log(r);
    //    r.text().then(text =>
    //    localStorage.setItem('myUserName', text));
    //});
    localStorage.setItem('myUserName', 'flinnfx#101')
    //let req = new XMLHttpRequest()
    //req.open('GET', 'http://127.0.0.1:5000/get_my_username')
    //req.setRequestHeader('Cross-Origin-Recourse-Policy', 'no-cors')
    //req.setRequestHeader('Access-Control-Allow-Origin', 'True')

    //req.send()
    //console.log(req.response)
    return 'flinnfx#101'
}

function get_own_username() {
    const username = localStorage.getItem('myUserName');
    if(username === null) {
        return fetch_username_from_api();
    } else {
        return username
    }
}

function Message(message: ClassicMessage) {
    if(message.from === get_own_username()) {
        return (
            <div key={gen_key_from_ClassicMessage(message)} className="SentMessageBox">
                <div className="SMessage">
                    {
                    // Add Styling so the Message actually looks good
                    }
                    <p>{gen_key_from_ClassicMessage(message)}</p>
                </div>
            </div>
        )
    } else {
        return (
            <div key={gen_key_from_ClassicMessage(message)} className="ReceivedMessageBox">
                <div className="RMessage">
                    {
                    // Add Styling so the Message actually looks good
                    }
                <p>{gen_key_from_ClassicMessage(message)}</p>
                </div>
            </div>
        )
    }

}

class ChatWindow extends React.Component<{}, {messages: Array<ClassicMessage>}> {
    UpdateTimer: NodeJS.Timer | undefined = undefined
    constructor(args: any) {
        super(args);
        this.state = {messages: this.fetch_messages()}
    }

    componentDidMount() {
        this.UpdateTimer = setInterval(() => this.update_messages(),500);
    }

    componentWillUnmount() {
        clearInterval(this.UpdateTimer)
    }


    update_messages() {
        this.setState({messages: this.fetch_messages()});
    }

    fetch_messages() {
        const Message1 = new ClassicMessage('flinnfx#101', 'tcgamer#102', 'This is some random Junk', '21 Dez 2021 11:50:11')
        const Message2 = new ClassicMessage('tcgamer#102','flinnfx#101', 'This is way more junk', '21 Dez 2021 11:51:22')

        const msgs: Array<ClassicMessage> = [Message1, Message2];
        return msgs
    }

    render() {
        const messages = this.state.messages
        console.log(typeof messages)
        console.log(messages)
        return (
                <div key="ChatWindowMainKey" id="ChatWindowMain">
                    {Sidebar.Sidebar(Sidebar.example_contacts)}
                    {messages.map(function (message, i) {
                        return Message(message);
                    })}
                </div>
        )
    }

}

export default ChatWindow