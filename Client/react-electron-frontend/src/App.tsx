import Chatwindow from './Chatwindow'



function AppContext() {
    return (
        <div className="background">
            <div className="foreground">
                {Chatwindow()}
            </div>
        </div>
    )
}

export default AppContext;