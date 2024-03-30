### Testing file ###
    # connect to anSQLite database or create in  the first instance
    # conn = sqlite3.connect('clinical_trials.db')
    # cursor = conn.cursor()

    # # make the studies table
    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS studies (
    #     nct_id TEXT PRIMARY KEY,
    #     company TEXT,
    #     sponsor_type TEXT,
    #     enrollment_count INTEGER,
    #     status TEXT
    # )
    # ''')

    # # iterate through datq and insert each study into the database
    # for nct_id, study_info in processor.studies.items():
    #     try:
    #         cursor.execute('''
    #         INSERT INTO studies (nct_id, company, sponsor_type, enrollment_count, status) 
    #         VALUES (?, ?, ?, ?, ?)
    #         ''', (nct_id, study_info['company'], study_info['sponsor_type'], study_info['enrollment_count'], study_info['status']))
    #     except sqlite3.IntegrityError as e:
    #         logger.error(f"Failed to insert {nct_id}: {e}")

    # # commit the changes and close the database connection
    # conn.commit()
    # conn.close()
    # logger.info("All studies have been succesfully stored in the database.")


