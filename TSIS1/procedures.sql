-- The procedure for adding a phone number to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE first_name = p_contact_name LIMIT 1;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    END IF;
END; $$;

-- The procedure for changing a group creates a group if it does not exist.
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_group_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name;
END; $$;

-- Advanced search function across all fields
CREATE OR REPLACE FUNCTION search_contacts_extended(p_query TEXT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, all_phones TEXT, group_name VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.email, string_agg(p.phone || ' (' || p.type || ')', ', '), g.name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.email      ILIKE '%' || p_query || '%'
       OR p.phone      ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END; $$;