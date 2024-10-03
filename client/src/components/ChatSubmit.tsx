import React, { useCallback, useRef, useState } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { LuSend } from "react-icons/lu";
import { Message } from "@/lib/types";
import { user_query } from "@/actions/getUserQuery";

interface ChatSubmitProps {
  setMessageHistory: React.Dispatch<React.SetStateAction<Message[] | []>>;
  setThinking: React.Dispatch<React.SetStateAction<boolean>>;
}

/**
 * Component that handles sending a message to the websocket server, and updating the message state
 * @param sendMessage: Function to send a message to the WebSocket server 
 * @returns Input and button to submit a message to the server
 */
const ChatSubmit: React.FC<ChatSubmitProps> = ({ setMessageHistory, setThinking }) => {
  const [message, setMessage] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);

  // Submit a message callback
  const handleSubmit = useCallback(async () => {
    if (!message) return;
    setThinking((prev) => !prev)
    setMessageHistory((prev) => [...prev, { type: 1, data: message }]);
    console.log('hi')
    const res = await user_query(message);
    setMessageHistory((prev) => [...prev, { type: 0, data: res }]);
    setThinking((prev) => !prev)
    setMessage(""); 
  }, [message, setMessageHistory]);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSubmit(); // Call handleSubmit on Enter key press
      setMessage("")
    }
  };

  return (
    <div className="flex w-full max-w-3xl items-center space-x-5">
      <Input
        className="bg-zinc-700 w-full text-white border-0 placeholder:text-zinc-400 focus-visible::outline-none focus-visible:ring-0 rounded-full text-lg px-7 py-7"
        ref={inputRef}
        value={message}
        placeholder="What do you need help with?"
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => handleKeyDown(e)}
      />
      <Button
        type="submit"
        onClick={() => handleSubmit()}
        className="rounded-full h-[56px] w-[56px]"
        disabled={message == ""}
      >
        <LuSend size = {56} />
      </Button>
    </div>
  );
};

export default ChatSubmit;
