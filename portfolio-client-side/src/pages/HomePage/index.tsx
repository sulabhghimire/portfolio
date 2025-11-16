import { useRef, useState } from "react";
import Avatar from "../../components/Avatar";
import Input from "../../components/TextInput";
import Button from "../../components/Button";
import { Send, Sparkles } from "lucide-react";
import AnimatedSparkleBadge from "../../components/Assitant";

const getResponse = (userMessage: string): string => {
  const lowerMessage = userMessage.toLowerCase();

  if (lowerMessage.includes("hello") || lowerMessage.includes("hi")) {
    return "Hello! I'm Sulabh Ghimire's AI assistant. I can tell you about Sulabh's experience, skills, projects, and more. What would you like to know?";
  }

  if (lowerMessage.includes("experience") || lowerMessage.includes("work")) {
    return "Sulabh Ghimire is a Software Engineer with extensive experience in full-stack development. He has worked on various projects involving modern web technologies, cloud infrastructure, and scalable applications. His expertise includes building robust backend systems and intuitive user interfaces.";
  }

  if (lowerMessage.includes("skill") || lowerMessage.includes("technology") || lowerMessage.includes("tech stack")) {
    return "Sulabh is proficient in:\n\n• Frontend: React, TypeScript, Next.js, Tailwind CSS\n• Backend: Node.js, Python, Java\n• Databases: PostgreSQL, MongoDB, Redis\n• Cloud & DevOps: AWS, Docker, Kubernetes\n• Tools: Git, CI/CD, Agile methodologies\n\nHe's passionate about writing clean, maintainable code and staying updated with the latest technologies.";
  }

  if (lowerMessage.includes("project")) {
    return "Sulabh has worked on several notable projects:\n\n1. E-commerce Platform - Built a scalable e-commerce solution handling thousands of transactions\n2. Real-time Analytics Dashboard - Developed a data visualization platform for business insights\n3. API Gateway Service - Designed and implemented a microservices architecture\n4. Mobile App Backend - Created RESTful APIs for a cross-platform mobile application\n\nEach project demonstrates his ability to solve complex technical challenges.";
  }

  if (lowerMessage.includes("education") || lowerMessage.includes("study")) {
    return "Sulabh holds a degree in Computer Science and continuously invests in learning new technologies through online courses, certifications, and hands-on projects. He believes in lifelong learning and staying current with industry trends.";
  }

  if (lowerMessage.includes("contact") || lowerMessage.includes("reach") || lowerMessage.includes("email")) {
    return "You can reach Sulabh Ghimire through:\n\n• Email: sulabh.ghimire@example.com\n• LinkedIn: linkedin.com/in/sulabhghimire\n• GitHub: github.com/sulabhghimire\n\nFeel free to connect for collaboration opportunities or just to chat about technology!";
  }

  if (lowerMessage.includes("who are you") || lowerMessage.includes("about")) {
    return "I'm Sulabh Ghimire, a passionate Software Engineer dedicated to building innovative solutions that make a difference. With a strong foundation in computer science and years of hands-on experience, I specialize in creating scalable, user-friendly applications. I love tackling challenging problems and collaborating with teams to deliver high-quality software.";
  }

  return "That's an interesting question! While this is a demo portfolio, in a real implementation, I would connect to a backend API to provide more detailed and personalized responses. Feel free to ask about Sulabh's experience, skills, projects, education, or how to get in touch!";
};

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const HomePage = () => {

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate API call delay
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: getResponse(userMessage.content),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 800);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

    return (
        <div className="flex-1 h-full overflow-hidden p-10">
          <div className="h-full flex flex-col items-center justify-center px-4 pb-32">
            <div className="w-full max-w-2xl space-y-8">
              <div className="text-center space-y-4">
               <AnimatedSparkleBadge/>
                <h2 className="text-zinc-900 dark:text-zinc-100">
                  Hi, I'm Sulabh Ghimire's AI Assistant
                </h2>
                <p className="text-zinc-600 dark:text-zinc-400">
                  Software Engineer passionate about building innovative solutions.
                  Ask me anything about my experience, skills, or projects!
                </p>
              </div>

              <div className="space-y-3">
                <div className="flex gap-2">
                  <Input
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Ask me about Sulabh Ghimire"
                    className="flex-1 px-2
                    border rounded
                  bg-zinc-50 text-zinc-600 dark:bg-zinc-900 
                  placeholder:text-zinc-500 dark:border-zinc-800 border-zinc-200
                  dark:placeholder:text-zinc-400
                    focus-visible:outline-none
                    focus-visible:ring-2
                  focus-visible:ring-zinc-300/50
                  dark:focus-visible:ring-zinc-500/40
                  focus-visible:border-zinc-400
                  dark:focus-visible:border-zinc-500
                     "
                    disabled={isLoading}
                  />
                  <Button
                    onClick={handleSend}
                    disabled={!input.trim() || isLoading}
                    size="icon"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <button
                    onClick={() => setInput("Tell me about your experience")}
                    className="p-3 text-left rounded-lg border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-colors text-zinc-700 dark:text-zinc-300"
                  >
                    Tell me about your experience
                  </button>
                  <button
                    onClick={() => setInput("What are your technical skills?")}
                    className="p-3 text-left rounded-lg border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-colors text-zinc-700 dark:text-zinc-300"
                  >
                    What are your technical skills?
                  </button>
                  <button
                    onClick={() => setInput("Show me your projects")}
                    className="p-3 text-left rounded-lg border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-colors text-zinc-700 dark:text-zinc-300"
                  >
                    Show me your projects
                  </button>
                  <button
                    onClick={() => setInput("How can I contact you?")}
                    className="p-3 text-left rounded-lg border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-colors text-zinc-700 dark:text-zinc-300"
                  >
                    How can I contact you?
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
    )
}

export default HomePage;