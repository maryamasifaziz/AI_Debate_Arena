from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .agents import con_agent, judge_agent, pro_agent
from .models import DebateMessage, DebateRoom

def _history_for_llm(room, limit=12):
    qs = room.messages.exclude(role="system").order_by("-created_at")[:limit]
    items = list(reversed(qs))
    history = []
    for m in items:
        if m.role in ("student",):
            history.append({"role": "user", "content": m.content})
        else:
            history.append({"role": "assistant", "content": f"{m.get_role_display()}: {m.content}"})
    return history

@login_required
def home(request):
    room = DebateRoom.objects.filter(owner=request.user).order_by("-created_at").first()
    if not room:
        room = DebateRoom.objects.create(owner=request.user, title="My Debate Room")
        DebateMessage.objects.create(room=room, role="system", content="Welcome. Start a debate by typing a topic and your statement.")
    return redirect("room", room_id=room.id)

@login_required
def room(request, room_id):
    room = get_object_or_404(DebateRoom, id=room_id, owner=request.user)
    rooms = DebateRoom.objects.filter(owner=request.user).order_by("-created_at")
    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == "new_room":
            title = (request.POST.get("title") or "My Debate Room").strip()[:120]
            new_room = DebateRoom.objects.create(owner=request.user, title=title or "My Debate Room")
            DebateMessage.objects.create(room=new_room, role="system", content="New room created. Start your debate.")
            return redirect("room", room_id=new_room.id)

        if action == "send":
            topic = (request.POST.get("topic") or "").strip()
            text = (request.POST.get("text") or "").strip()
            mode = request.POST.get("mode") or "student_vs_ai"
            student_side = request.POST.get("student_side") or "pro"
            if not topic or not text:
                messages.error(request, "Topic aur message dono zaroori hain.")
                return redirect("room", room_id=room.id)

            DebateMessage.objects.create(room=room, role="student", content=f"{topic} {text}")

            history = _history_for_llm(room)
            try:
                if mode == "student_vs_ai":
                    if student_side == "pro":
                        ai_text = con_agent(topic, history)
                        DebateMessage.objects.create(room=room, role="con", content=ai_text)
                    else:
                        ai_text = pro_agent(topic, history)
                        DebateMessage.objects.create(room=room, role="pro", content=ai_text)

                if mode == "ai_vs_ai":
                    pro_text = pro_agent(topic, history)
                    DebateMessage.objects.create(room=room, role="pro", content=pro_text)
                    con_text = con_agent(topic, history + [{"role": "assistant", "content": f"ProAgent: {pro_text}"}])
                    DebateMessage.objects.create(room=room, role="con", content=con_text)
                    j = judge_agent(topic, pro_text, con_text)
                    DebateMessage.objects.create(room=room, role="judge", content=j)

            except Exception as e:
                messages.error(request, f"AI error: {e}")

            return redirect("room", room_id=room.id)

    return render(request, "debate/arena.html", {"room": room, "rooms": rooms, 
                                                 "ai_provider": getattr(settings, "AI_PROVIDER","groq"),
                                                 "groq_model": getattr(settings, "GROQ_MODEL","openai/gpt-oss-20b"),
                                                 "openai_model": getattr(settings,"OPENAI_MODEL","gpt-5"),})

@login_required
def clear_room(request, room_id):
    if request.method != "POST":
        return redirect("room", room_id=room_id)
    room = get_object_or_404(DebateRoom, id=room_id, owner=request.user)
    room.messages.exclude(role="system").delete()
    messages.success(request, "Room clear ho gaya.")
    return redirect("room", room_id=room.id)