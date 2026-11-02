# -*- coding: utf-8 -*-
"""Écrit les lots de test des Parts 3, 4, 6 et 7 dans tests/donnees/banque (à relancer seulement pour les changer)."""
import json
import os

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banque")


def dump(name, sets):
    with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"sets": sets}, ensure_ascii=False, indent=2) + "\n")


P3 = [
    {"id": "3t-001", "speakers": {"W": "f", "M": "m"},
     "lines": [["W", "Hi, Daniel. Did you get a chance to look at the revised budget for the trade fair?"],
               ["M", "I did. The booth rental went up, but we saved on printing by ordering the brochures online."],
               ["W", "Good. What about travel? Four of us are going to Chicago."],
               ["M", "Flights are booked. The hotel is the only thing left, and the cheaper one near the venue is full."],
               ["W", "Then let’s ask the organizers. They usually reserve rooms for exhibitors at a discount."],
               ["M", "Good idea. I’ll call them this afternoon."]],
     "lines_fr": ["Salut Daniel. Tu as pu regarder le budget révisé du salon ?",
                  "Oui. La location du stand a augmenté, mais on a économisé sur l’impression en commandant les brochures en ligne.",
                  "Bien. Et le voyage ? Nous allons à Chicago à quatre.",
                  "Les vols sont réservés. Il ne reste que l’hôtel, et le moins cher, près du lieu, est complet.",
                  "Alors demandons aux organisateurs. Ils réservent souvent des chambres à prix réduit pour les exposants.",
                  "Bonne idée. Je les appelle cet après-midi."],
     "graphic": None,
     "questions": [
         {"q": "What event are the speakers preparing for?", "opts": ["A product launch", "A trade fair", "A training session", "A job fair"],
          "ans": "B", "type": "sujet", "expl": "La femme parle du *budget for the trade fair*.", "q_fr": "À quel événement les interlocuteurs se préparent-ils ?"},
         {"q": "How did the speakers reduce costs?", "opts": ["By sharing a booth", "By choosing a cheaper hotel", "By ordering brochures online", "By flying economy"],
          "ans": "C", "type": "detail", "expl": "*We saved on printing by ordering the brochures online.* L’hôtel bon marché est complet : piège.",
          "q_fr": "Comment les interlocuteurs ont-ils réduit les coûts ?"},
         {"q": "What will the man do this afternoon?", "opts": ["Contact the organizers", "Book flights", "Print brochures", "Visit the venue"],
          "ans": "A", "type": "action", "expl": "*I’ll call them this afternoon* : *them* reprend *the organizers*.", "q_fr": "Que va faire l’homme cet après-midi ?"}]},
    {"id": "3t-002", "speakers": {"W": "f", "M": "m", "M2": "m"},
     "lines": [["M", "Priya, Tom, the client moved the presentation to Thursday morning."],
               ["W", "Thursday? The slides won’t be ready by then."],
               ["M2", "I can finish the charts tonight if Priya sends me the sales figures."],
               ["W", "I’ll send them right after this meeting."],
               ["M", "Great. Then let’s rehearse on Wednesday afternoon, after lunch."],
               ["M2", "Room B is booked all day, so we’ll need another room. The schedule is on the board."]],
     "lines_fr": ["Priya, Tom, le client a avancé la présentation à jeudi matin.", "Jeudi ? Les diapositives ne seront pas prêtes.",
                  "Je peux finir les graphiques ce soir si Priya m’envoie les chiffres de ventes.", "Je les envoie juste après cette réunion.",
                  "Parfait. Alors répétons mercredi après-midi, après le déjeuner.",
                  "La salle B est réservée toute la journée, il nous faudra une autre salle. Le planning est au tableau."],
     "graphic": {"title": "Room availability, Wednesday", "rows": [["Room", "Free"], ["Room A", "9:00 to 11:00"], ["Room B", "Booked all day"], ["Room C", "2:00 to 5:00"]]},
     "questions": [
         {"q": "Why is the woman concerned?", "opts": ["A client canceled a meeting", "Some slides may not be finished", "A room is too small", "Sales have fallen"],
          "ans": "B", "type": "inference", "expl": "*The slides won’t be ready by then* : elle craint de ne pas finir à temps.", "q_fr": "Pourquoi la femme est-elle inquiète ?"},
         {"q": "What does the woman agree to do?", "opts": ["Rehearse alone", "Call the client", "Send some figures", "Prepare the charts"],
          "ans": "C", "type": "action", "expl": "Tom demande les chiffres de ventes ; elle répond *I’ll send them right after this meeting*.",
          "q_fr": "Qu’est-ce que la femme accepte de faire ?"},
         {"q": "Look at the graphic. Which room will the speakers most likely use?", "opts": ["Room A", "Room B", "Room C", "The client’s office"],
          "ans": "C", "type": "graphique", "expl": "Ils répètent mercredi après-midi et la salle B est prise : seule la salle C est libre l’après-midi (2:00 to 5:00).",
          "q_fr": "Regardez le graphique. Quelle salle les interlocuteurs vont-ils sans doute utiliser ?"}]},
]

P4 = [
    {"id": "4t-001", "speakers": {"W": "f"},
     "lines": [["W", "Good morning, and welcome to the Harbor Museum."],
               ["W", "Before we begin the tour, please note that photography is allowed in every gallery except the map room."],
               ["W", "The tour lasts about an hour and ends at the gift shop on the ground floor."],
               ["W", "Since the elevator is being repaired today, we will take the stairs to the second floor."],
               ["W", "If you need a break at any point, there are benches in each gallery. Now, let’s get started."]],
     "lines_fr": ["Bonjour et bienvenue au musée du Port.",
                  "Avant de commencer la visite, notez que les photos sont permises dans toutes les salles sauf la salle des cartes.",
                  "La visite dure environ une heure et se termine à la boutique du rez-de-chaussée.",
                  "Comme l’ascenseur est en réparation aujourd’hui, nous prendrons l’escalier jusqu’au deuxième étage.",
                  "Si vous avez besoin d’une pause, il y a des bancs dans chaque salle. Allons-y."],
     "graphic": None,
     "questions": [
         {"q": "Who most likely is the speaker?", "opts": ["A shop assistant", "A tour guide", "A photographer", "An elevator technician"],
          "ans": "B", "type": "sujet", "expl": "Elle accueille les visiteurs et annonce *the tour* : c’est une guide.", "q_fr": "Qui est sans doute l’oratrice ?"},
         {"q": "Where is photography not permitted?", "opts": ["In the gift shop", "On the stairs", "In the map room", "On the second floor"],
          "ans": "C", "type": "detail", "expl": "*Photography is allowed in every gallery except the map room.*", "q_fr": "Où est-il interdit de photographier ?"},
         {"q": "Why does the speaker say, “there are benches in each gallery”?",
          "opts": ["To describe the museum’s furniture", "To ask visitors to sit down", "To reassure listeners who may get tired", "To explain a new exhibit"],
          "ans": "C", "type": "intention", "expl": "Elle répond à *If you need a break* : elle rassure ceux qui seraient fatigués.",
          "q_fr": "Pourquoi l’oratrice dit-elle « il y a des bancs dans chaque salle » ?"}]},
]

P6 = [
    {"id": "6t-001", "kind": "e-mail",
     "text": "To: All staff\nFrom: Facilities Department\nSubject: Parking garage\n\nDear colleagues,\n\nStarting Monday, the north entrance of the parking garage "
             "will be closed [1] repairs. Please use the south entrance on Pine Street instead. [2]\n\nWe expect the work to be completed within two weeks. "
             "During this period, the number of available spaces will be [3] reduced, so we encourage you to carpool or take public transportation. "
             "Your patience is [4] appreciated.\n\nFacilities Department",
     "text_fr": "À : tout le personnel\nDe : service des locaux\nObjet : parking\n\nChers collègues,\n\nÀ partir de lundi, l’entrée nord du parking sera fermée "
                "pour travaux. Merci d’utiliser l’entrée sud, rue Pine. Elle sera ouverte de 6 h à 22 h.\n\nNous pensons terminer les travaux en deux semaines. "
                "Pendant cette période, le nombre de places sera nettement réduit : nous vous encourageons donc au covoiturage ou aux transports en commun. "
                "Merci beaucoup de votre patience.\n\nService des locaux",
     "questions": [
         {"opts": ["for", "since", "during", "until"], "ans": "A", "type": "prep", "expl": "*Closed for repairs* : fermé pour travaux (le motif)."},
         {"opts": ["The garage was built ten years ago.", "It will be open from 6 A.M. to 10 P.M.", "Parking fees will increase next month.", "Visitors must register at reception."],
          "ans": "B", "type": "phrase", "expl": "La phrase donne les horaires de l’entrée sud qu’on vient de citer ; les autres n’ont pas de lien avec ce qui précède."},
         {"opts": ["significance", "significant", "significantly", "signify"], "ans": "C", "type": "forme", "expl": "Un adverbe modifie l’adjectif *reduced* : *significantly*."},
         {"opts": ["great", "greater", "greatness", "greatly"], "ans": "D", "type": "forme", "expl": "Un adverbe modifie le participe *appreciated* : *greatly appreciated*."}]},
]

P7 = [
    {"id": "7t-001", "docs": [{"kind": "article", "title": "Harbor City Expands Ferry Service",
                                "text": "Harbor City will add two ferry routes next spring, the transit authority announced on Tuesday. [1] The new routes will connect "
                                        "the downtown pier with Bayview and the airport.\n\nThe authority expects the routes to carry 3,000 passengers a day. [2] "
                                        "Tickets will cost the same as a bus fare. [3] Construction of a second dock at the airport begins in March. [4]",
                                "table": None}],
     "docs_fr": ["Harbor City va ajouter deux lignes de ferry au printemps prochain, a annoncé mardi l’autorité des transports. Les nouvelles lignes "
                 "relieront l’embarcadère du centre à Bayview et à l’aéroport.\n\nL’autorité prévoit 3 000 passagers par jour. Le billet coûtera le prix d’un "
                 "ticket de bus. La construction d’un second quai à l’aéroport commence en mars."],
     "questions": [
         {"q": "What is the article mainly about?", "opts": ["New ferry routes", "A new airport", "Higher bus fares", "A dock closure"],
          "ans": "A", "type": "idee", "expl": "Tout l’article décrit les deux nouvelles lignes de ferry.", "q_fr": "De quoi parle surtout l’article ?"},
         {"q": "In which of the positions marked [1], [2], [3], and [4] does the following sentence best belong? “Monthly passes will also be accepted.”",
          "opts": ["[1]", "[2]", "[3]", "[4]"], "ans": "C", "type": "insertion",
          "expl": "La phrase complète l’information sur le prix : elle vient juste après *Tickets will cost the same as a bus fare*.",
          "q_fr": "À laquelle des positions [1], [2], [3] et [4] la phrase suivante s’insère-t-elle le mieux ? « Les abonnements mensuels seront aussi acceptés. »"}]},
    {"id": "7t-002", "docs": [
        {"kind": "annonce", "title": "Weekend workshops", "text": "Riverside Library offers free workshops on Saturdays. Registration is required.",
         "table": {"title": "June workshops", "rows": [["Date", "Workshop"], ["June 7", "Writing a résumé"], ["June 14", "Online banking"], ["June 21", "Smartphone photography"]]}},
        {"kind": "e-mail", "title": None,
         "text": "To: Riverside Library\nFrom: Ana Ruiz\n\nHello,\n\nI would like to register for the workshop on online banking. I am also interested in the "
                 "photography class, but I will be traveling that weekend. Will it be offered again?\n\nAna Ruiz", "table": None}],
     "docs_fr": ["La bibliothèque Riverside propose des ateliers gratuits le samedi. Inscription obligatoire.\nAteliers de juin : 7 juin, rédiger un CV ; "
                 "14 juin, banque en ligne ; 21 juin, photo au smartphone.",
                 "À : bibliothèque Riverside\nDe : Ana Ruiz\n\nBonjour,\n\nJe souhaite m’inscrire à l’atelier sur la banque en ligne. La photo m’intéresse aussi, "
                 "mais je serai en voyage ce week-end-là. Sera-t-il proposé à nouveau ?\n\nAna Ruiz"],
     "questions": [
         {"q": "What is indicated about the workshops?", "opts": ["They are held on weekdays.", "They are free of charge.", "They are taught online.", "They require no registration."],
          "ans": "B", "type": "vrai-faux", "expl": "*Free workshops on Saturdays. Registration is required.*", "q_fr": "Qu’apprend-on sur les ateliers ?"},
         {"q": "Which workshop will Ms. Ruiz attend?", "opts": ["Writing a résumé", "Online banking", "Smartphone photography", "Public speaking"],
          "ans": "B", "type": "detail", "expl": "*I would like to register for the workshop on online banking.*", "q_fr": "À quel atelier Mme Ruiz va-t-elle assister ?"},
         {"q": "When will Ms. Ruiz most likely be traveling?", "opts": ["June 7", "June 14", "June 21", "June 28"],
          "ans": "C", "type": "croise", "expl": "Elle voyage le week-end de l’atelier photo, le 21 juin d’après le tableau.", "q_fr": "Quand Mme Ruiz sera-t-elle sans doute en voyage ?"},
         {"q": "What does Ms. Ruiz ask about?", "opts": ["A refund", "A future session", "A meeting room", "A library card"],
          "ans": "B", "type": "detail", "expl": "*Will it be offered again?* : elle demande s’il y aura une autre session.", "q_fr": "Sur quoi Mme Ruiz pose-t-elle une question ?"},
         {"q": "In the e-mail, the word “interested” is closest in meaning to", "opts": ["curious", "invested", "concerned", "involved"],
          "ans": "A", "type": "vocab", "expl": "*Interested in* : intéressé par, curieux de. *Invested* garde la forme du mot sans le sens.",
          "q_fr": "Dans le courriel, le mot « interested » a le sens le plus proche de"}]},
]

if __name__ == "__main__":
    dump("part3-t.json", P3)
    dump("part4-t.json", P4)
    dump("part6-t.json", P6)
    dump("part7-t.json", P7)
    path = os.path.join(HERE, "banque.json")
    cfg = json.load(open(path, encoding="utf-8"))
    have = {e["id"] for e in cfg["listes"]}
    for e in [{"id": "3t", "type": "part3", "nom": "Part 3, test", "fichier": "part3-t.json"},
              {"id": "4t", "type": "part4", "nom": "Part 4, test", "fichier": "part4-t.json"},
              {"id": "6t", "type": "part6", "nom": "Part 6, test", "fichier": "part6-t.json"},
              {"id": "7t", "type": "part7", "nom": "Part 7, test", "fichier": "part7-t.json"}]:
        if e["id"] not in have:
            cfg["listes"].append(e)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
    print("lots de test écrits")
