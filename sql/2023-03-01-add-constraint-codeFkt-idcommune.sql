ALTER TABLE public.fokontany
  ADD CONSTRAINT uk_code_fkt_idcom UNIQUE (codefokontany, idcommune);
  
ALTER TABLE public.hameau
  ADD CONSTRAINT uk_codeham_idfkt UNIQUE (codehameau, idfokontany);