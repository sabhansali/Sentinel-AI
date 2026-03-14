from scapy.all import sniff
from scapy.layers.dns import DNSQR

from detector import detect_ai_tool
from process_detector import detect_ide_usage
from notifier import notify_backend
from config import ENABLE_BACKEND_NOTIFICATION

seen_domains = set()

def process_packet(packet):

    try:

        if packet.haslayer(DNSQR):

            domain = packet[DNSQR].qname.decode().strip(".")

            event = detect_ai_tool(domain)

            if event and domain not in seen_domains:

                ide_process = detect_ide_usage()

                print("\n====================================")
                print("⚠ SHADOW AI ACTIVITY DETECTED")
                print("Tool   :", event["tool"])
                print("Domain :", event["domain"])

                # If IDE running → possible Copilot usage
                if ide_process:
                    print("IDE    :", ide_process)
                    print("Mode   : AI-assisted coding")

                else:
                    print("Mode   : Browser AI usage")

                print("====================================\n")

                # Enrich event before sending
                event["ide_process"] = ide_process

                if ENABLE_BACKEND_NOTIFICATION:
                    notify_backend(event)

                seen_domains.add(domain)

    except Exception as e:

        print("Packet processing error:", e)


def start_sniffing():

    print("====================================")
    print(" Shadow AI DNS Monitor Started ")
    print("====================================")

    print("🔍 DNS Monitor Running...\n")

    sniff(
        filter="udp port 53",
        prn=process_packet,
        store=False
    )