INSERT INTO ACT_ANAGRAFICA_PIANTE_TESTATA (ID_PIANTA, ID_STATO_PIANTA, ID_ULTIMO_PROGRAMMA_ESEGUITO, DATA_INSERIMENTO, DATA_ULTIMA_MODIFICA)
VALUES ('87cfdbfb-8183-4952-95d7-651a0ca02c0c', 'BAGNATO', 'd9f70589-c4c9-419a-8e79-45d9a7203b40', '2025-11-25T22:33:51', '2025-11-25T22:33:51'),
        ('d68d69ea-c067-4063-9067-da6ecc8b84f5', 'BAGNATO', 'd9f70589-c4c9-419a-8e79-45d9a7203b40', '2025-11-24T23:02:42', '2025-11-24T23:02:42'),
        ('e5e8f1a7-75da-4e68-be8d-a0085ccb63ba', 'TROPPO_SECCO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-24T22:19:49', '2025-11-24T22:19:49'),
        ('dcd319b6-41a6-4054-be26-705ca96d6308', 'SECCO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-24T20:44:40', '2025-11-24T20:44:40'),
        ('09586468-a7b7-409b-80d3-7aab98f110b2', 'UMIDO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-24T20:19:56', '2025-11-24T20:19:56'),
        ('32c70991-171a-4e85-b22b-cae08f9dc0cc', 'UMIDO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-24T20:03:13', '2025-11-24T20:03:13'),
        ('c1e7f28e-4e36-48a3-a6b0-e3cf46d5101c', 'SECCO', 'd9f70589-c4c9-419a-8e79-45d9a7203b40', '2025-11-23T18:54:15', '2025-11-23T18:54:15'),
        ('41d2bcb7-e6f8-449e-8261-3bdb28a65e2c', 'SECCO', 'd9f70589-c4c9-419a-8e79-45d9a7203b40', '2025-11-23T22:51:58', '2025-11-23T22:51:58'),
        ('7bb60f76-9d90-492b-b985-1e920ebd0d5c', 'UMIDO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-18T21:19:46', '2025-11-18T21:19:46'),
        ('5c31b223-7cca-4395-a96b-bb9f89ad8b29', 'UMIDO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-18T21:18:36', '2025-11-18T21:18:36'),
        ('44de2a81-9b20-4b9a-b18e-4b97dfc697d1', 'TROPPO_BAGNATO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-18T20:06:05', '2025-11-18T20:06:05'),
        ('f7cd82b1-165c-48c4-8f1f-f42d5308141f', 'TROPPO_BAGNATO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-18T20:04:42', '2025-11-18T20:04:42'),
        ('f751de1f-44ea-4c38-9b11-477564ad3a34', 'SECCO', 'c0e5c1ea-413e-4af1-b514-a9b29d03fff0', '2025-11-18T19:38:58', '2025-11-18T19:38:58'),
        ('e800d543-359c-40ee-b61a-623e114ff404', 'TROPPO_SECCO', '65246103-ae4b-4e4d-baea-b4f9cbbb7203', '2025-11-12T22:19:19', '2025-11-12T22:19:19'),
        ('c72d7ca9-74c4-4b11-975b-677bab4d931a', 'BAGNATO', '65246103-ae4b-4e4d-baea-b4f9cbbb7203', '2025-11-11T20:03:28', '2025-11-11T20:03:28'),
        ('9dbb883e-cfbd-4d8b-b1fc-35e694ecbfba', 'BAGNATO', '65246103-ae4b-4e4d-baea-b4f9cbbb7203', '2025-11-10T23:58:57', '2025-11-10T23:58:57'),
        ('3be8bbe3-8559-44b4-a04b-83e1289f6b4a', 'BAGNATO', '65246103-ae4b-4e4d-baea-b4f9cbbb7203', '2025-11-10T23:55:34', '2025-11-10T23:55:34');



INSERT INTO ACT_ANAGRAFICA_PIANTE_DETTAGLIO (ID_PIANTA, NOME_PIANTA, DESCRIZIONE_PIANTA, FOTO_PIANTA, ID_STANZA, POSIZIONE_STANZA_X, POSIZIONE_STANZA_Y)
VALUES ('87cfdbfb-8183-4952-95d7-651a0ca02c0c', 'Basilico', 'Con cui Chry potrà avverare il proprio desiderio di fare il miglior pesto del MONDO.', '1a540395-a555-11f0-9cdc-9c5c8e86fa68', null, null),
        ('d68d69ea-c067-4063-9067-da6ecc8b84f5', 'Basilico', 'Con cui Chry potrà avverare il proprio desiderio di fare il miglior pesto del MONDO.', '1a540395-a555-11f0-9cdc-9c5c8e86fa68', null, null),
        ('e5e8f1a7-75da-4e68-be8d-a0085ccb63ba', 'Felce', 'Pianta che piace tanto a Christian, che starebbe benissimo su un vaso a forma di testa, ma poi farebbe sentire mio padre a disagio.', '2c1575dd-a555-11f0-9cdc-9c5c8e86fa68', 3, 5),
        ('dcd319b6-41a6-4054-be26-705ca96d6308', 'Piantina dell''IKEA', 'In realtà funge da portapenne, ma noi facciamo finta di innaffiarla per il content.', '31a32a11-f5fc-497e-8a27-0c6b6d645c0d', 1, 2),
        ('09586468-a7b7-409b-80d3-7aab98f110b2', 'Piantina dell''IKEA', 'In realtà funge da portapenne, ma noi facciamo finta di innaffiarla per il content.', '31a32a11-f5fc-497e-8a27-0c6b6d645c0d', 1, 2),
        ('32c70991-171a-4e85-b22b-cae08f9dc0cc', 'Palma', 'Sicuramente una palma non molto alta, con le scimmie all''interno, ma mini perché sta in appartamento.', '2c1575dd-a555-11f0-9cdc-9c5c8e86fa68', 1, 2),
        ('c1e7f28e-4e36-48a3-a6b0-e3cf46d5101c', 'Edera', 'Pianta pendente sopra la scrivania.', '1a540395-a555-11f0-9cdc-9c5c8e86fa68', 4, 3),
        ('41d2bcb7-e6f8-449e-8261-3bdb28a65e2c', 'Cactus', 'Pianta grassa che dicono non aver bisogno di acqua e poi comunque muore.', '1a540395-a555-11f0-9cdc-9c5c8e86fa68', 2, 1),
        ('7bb60f76-9d90-492b-b985-1e920ebd0d5c', 'Orchidea', 'Orchidea che fiorisce solo 15 giorni all''anno.', '2c1575dd-a555-11f0-9cdc-9c5c8e86fa68', 4, 3),
        ('5c31b223-7cca-4395-a96b-bb9f89ad8b29', 'Orchidea', 'Orchidea che fiorisce solo 15 giorni all''anno.', '2c1575dd-a555-11f0-9cdc-9c5c8e86fa68', 4, 3),
        ('44de2a81-9b20-4b9a-b18e-4b97dfc697d1', 'Orchidea', 'Orchidea che fiorisce solo 15 giorni all''anno.', '2c1575dd-a555-11f0-9cdc-9c5c8e86fa68', 4, 3),
        ('f7cd82b1-165c-48c4-8f1f-f42d5308141f', 'Orchidea', 'Orchidea che fiorisce solo 15 giorni all''anno.', '2c1575dd-a555-11f0-9cdc-9c5c8e86fa68', 4, 3),
        ('f751de1f-44ea-4c38-9b11-477564ad3a34', 'Orchidea', 'Orchidea che fiorisce solo 15 giorni all''anno.', '2c1575dd-a555-11f0-9cdc-9c5c8e86fa68', 4, 3),
        ('e800d543-359c-40ee-b61a-623e114ff404', 'Rosa rossa', 'Rosa rossa regalata al primo anniversario dall''amore mio grandissimo (non arancione che significa gelosia, a quanto pare).', '23fb1599-a555-11f0-9cdc-9c5c8e86fa68', 1, 2),
        ('c72d7ca9-74c4-4b11-975b-677bab4d931a', 'Rosa rossa', 'Rosa rossa regalata al primo anniversario dall''amore mio grandissimo (non arancione che significa gelosia, a quanto pare).', '23fb1599-a555-11f0-9cdc-9c5c8e86fa68', 1, 2),
        ('9dbb883e-cfbd-4d8b-b1fc-35e694ecbfba', 'Rosa rossa', 'Rosa rossa regalata al primo anniversario dall''amore mio grandissimo (non arancione che significa gelosia, a quanto pare).', '23fb1599-a555-11f0-9cdc-9c5c8e86fa68', 1, 2),
        ('3be8bbe3-8559-44b4-a04b-83e1289f6b4a', 'Rosa rossa', 'Rosa rossa regalata al primo anniversario dall''amore mio grandissimo (non arancione che significa gelosia, a quanto pare).', '23fb1599-a555-11f0-9cdc-9c5c8e86fa68', 1, 2);



--INSERT INTO ACT_ANAGRAFICA_PIANTE_DETTAGLIO_SENSORI (ID_PIANTA, UMIDITA_CORRENTE, ACQUA_ULTIMA_INNAFFIATURA, ALTRO_DATO_SENSORI_1, ALTRO_DATO_SENSORI_2, ALTRO_DATO_SENSORI_3, ALTRO_DATO_SENSORI_4)
