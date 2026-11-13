from command_router import CommandRouter


def run_test(name, command):

    try:

        result = router.handle(
            command
        )

        print(
            f"[OK] {name}"
        )

        print(
            result
        )

        print()

        return True

    except Exception as e:

        print(
            f"[FEHLER] {name}"
        )

        print(e)

        print()

        return False


router = CommandRouter()

print(
    "\n=== OPENJARVIS SELBSTTEST ===\n"
)

results = []

# --------------------
# GEDÄCHTNIS
# --------------------

results.append(

    run_test(
        "Name speichern",
        "merke name Michael"
    )
)

results.append(

    run_test(
        "Name lesen",
        "wie heiße ich"
    )
)

results.append(

    run_test(
        "Gedächtnis anzeigen",
        "zeige gedächtnis"
    )
)

# --------------------
# AUFGABEN
# --------------------

results.append(

    run_test(
        "Aufgabe anlegen",
        "neue aufgabe Selbsttest Aufgabe"
    )
)

results.append(

    run_test(
        "Aufgaben anzeigen",
        "zeige aufgaben"
    )
)

results.append(

    run_test(
        "Nächste Aufgabe",
        "was ist die nächste aufgabe"
    )
)

# --------------------
# PROJEKTE
# --------------------

results.append(

    run_test(
        "Projekt erstellen",
        "neues projekt SelbsttestProjekt"
    )
)

results.append(

    run_test(
        "Projektaufgabe anlegen",
        (
            "projektaufgabe "
            "SelbsttestProjekt | "
            "Projekt testen"
        )
    )
)

results.append(

    run_test(
        "Projekt anzeigen",
        "zeige projekt SelbsttestProjekt"
    )
)

results.append(

    run_test(
        "Projektstatus",
        "projektstatus SelbsttestProjekt"
    )
)

results.append(

    run_test(
        "Nächste Projektaufgabe",
        (
            "nächste projektaufgabe "
            "SelbsttestProjekt"
        )
    )
)

results.append(

    run_test(
        "Arbeite an Projekt",
        (
            "arbeite an projekt "
            "SelbsttestProjekt"
        )
    )
)

# --------------------
# DATEISYSTEM
# --------------------

results.append(

    run_test(
        "Directory Tree",
        "zeige baum F:\\Jarvis"
    )
)

# --------------------
# ABSCHLUSS
# --------------------

success_count = sum(results)

failure_count = (
    len(results)
    - success_count
)

print(
    "\n=== ERGEBNIS ===\n"
)

print(
    f"Bestanden: {success_count}"
)

print(
    f"Fehlgeschlagen: {failure_count}"
)

if failure_count == 0:

    print(
        "\n✅ ALLE TESTS BESTANDEN"
    )

else:

    print(
        "\n❌ FEHLER GEFUNDEN"
    )