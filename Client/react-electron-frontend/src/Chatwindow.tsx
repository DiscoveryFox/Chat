import Sidebar from "./Sidebar";
import React from "react";

const person1 = new Sidebar.ContactClass('Flinn', 2)
const person2 = new Sidebar.ContactClass('Alex', 1)
const contacts = [person1, person2]

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

function Message(message: ClassicMessage) {
    return (
        <div key={gen_key_from_ClassicMessage(message)}>
            {
                // Add Styling so the Message actually looks good
            }
            <p>{gen_key_from_ClassicMessage(message)}</p>
        </div>
    )
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
            <div>
                {messages.map(function (message, i) {
                    return Message(message);
                })}
            </div>
        )
    }

}

export default ChatWindow