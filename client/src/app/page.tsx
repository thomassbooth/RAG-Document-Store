"use client";

import ChatSubmit from "@/components/ChatSubmit";
import Container from "@/components/Container";
import Response from "@/components/Response";
import Thinking from "@/components/Thinking";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useEffect, useRef, useState } from "react";
import { Message } from "@/lib/types";

export default function Home() {
  const scrollRef = useRef(null);
  const [messageHistory, setMessageHistory] = useState<Message[] | []>([]);
  const [thinking, setThinking] = useState(false);


  useEffect(() => {
    if (scrollRef.current) {
      // @ts-expect-error - scrollRef is not typed
      scrollRef.current.scrollTo({
        // @ts-expect-error - scrollHeight is not typed
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messageHistory]);

  return (
    <div className="flex flex-col items-center justify-between pt-6">
      <section className="w-full flex flex-col items-center">
        <div className="mt-6 w-full">
          <ScrollArea ref={scrollRef} className="w-full h-[78vh] py-10">
            <Container>
              <div>
                <ul className="flex gap-2 w-full flex-wrap">
                  {messageHistory.map((msg, index) => (
                    <Response key={index} text={msg.data} type={msg.type} />
                  ))}
                </ul>
                {thinking && <Thinking />}
              </div>
            </Container>
          </ScrollArea>
        </div>
        <ChatSubmit setMessageHistory={setMessageHistory} setThinking = {setThinking}/>
        <span className="py-2">built by Thomas Booth</span>
      </section>
    </div>
  );
}
