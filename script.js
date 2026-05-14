document.addEventListener('DOMContentLoaded', () => {

  // ========== PRELOADER ==========
  const preloader = document.querySelector('.preloader');
  window.addEventListener('load', () => {
    setTimeout(() => preloader?.classList.add('hidden'), 800);
  });

  // ========== NAV SCROLL ==========
  const nav = document.querySelector('nav');
  const backTop = document.querySelector('.back-top');
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    nav?.classList.toggle('scrolled', y > 60);
    backTop?.classList.toggle('show', y > 500);
  });

  // ========== HAMBURGER ==========
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobileMenu.classList.toggle('open');
    document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
  });
  mobileMenu?.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });

  // ========== SCROLL REVEAL ==========
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); }});
  }, { threshold: 0.15 });
  reveals.forEach(el => revealObs.observe(el));

  // ========== COUNTER ANIMATION ==========
  const counters = document.querySelectorAll('[data-count]');
  const countObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const el = e.target;
        const target = parseInt(el.dataset.count);
        const suffix = el.dataset.suffix || '';
        const prefix = el.dataset.prefix || '';
        let current = 0;
        const step = Math.ceil(target / 60);
        const timer = setInterval(() => {
          current += step;
          if (current >= target) { current = target; clearInterval(timer); }
          el.textContent = prefix + current.toLocaleString('pt-BR') + suffix;
        }, 25);
        countObs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(el => countObs.observe(el));

  // ========== FAQ ACCORDION ==========
  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });

  // ========== PRICING TOGGLE ==========
  const toggle = document.querySelector('.toggle-switch');
  const monthLabel = document.querySelector('.month-label');
  const yearLabel = document.querySelector('.year-label');
  toggle?.addEventListener('click', () => {
    toggle.classList.toggle('annual');
    const isAnnual = toggle.classList.contains('annual');
    monthLabel?.classList.toggle('active', !isAnnual);
    yearLabel?.classList.toggle('active', isAnnual);
    document.querySelectorAll('.plan').forEach(plan => {
      const monthly = plan.dataset.monthly;
      const annual = plan.dataset.annual;
      const priceEl = plan.querySelector('.price-val');
      const periodEl = plan.querySelector('.period');
      if (priceEl && monthly && annual) {
        priceEl.innerHTML = isAnnual ? `<small>R$</small>${annual}` : `<small>R$</small>${monthly}`;
        periodEl.textContent = isAnnual ? '/ano (economia de 20%)' : '/mês';
      }
    });
  });

  // ========== CART SYSTEM ==========
  let cart = JSON.parse(localStorage.getItem('cs_cart') || '[]');

  const cartSidebar = document.querySelector('.cart-sidebar');
  const cartOverlay = document.querySelector('.cart-overlay');
  const cartItemsEl = document.querySelector('.cart-items');
  const cartCountEls = document.querySelectorAll('.cart-count');
  const cartTotalEl = document.querySelector('.cart-total .val');

  function openCart() {
    cartSidebar?.classList.add('open');
    cartOverlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeCart() {
    cartSidebar?.classList.remove('open');
    cartOverlay?.classList.remove('open');
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.cart-btn').forEach(b => b.addEventListener('click', openCart));
  document.querySelector('.cart-close')?.addEventListener('click', closeCart);
  cartOverlay?.addEventListener('click', closeCart);

  function saveCart() { localStorage.setItem('cs_cart', JSON.stringify(cart)); }

  function updateCartUI() {
    const count = cart.reduce((s, i) => s + i.qty, 0);
    cartCountEls.forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
    if (!cartItemsEl) return;
    if (cart.length === 0) {
      cartItemsEl.innerHTML = '<div class="cart-empty"><span class="empty-icon">🔑</span>Seu carrinho está vazio</div>';
      if (cartTotalEl) cartTotalEl.textContent = 'R$ 0,00';
      return;
    }
    let html = '';
    cart.forEach((item, idx) => {
      html += `<div class="cart-item">
        <div class="cart-item-img">${item.icon}</div>
        <div class="cart-item-info">
          <h4>${item.name}</h4>
          <span class="cart-item-price">R$ ${item.price.toFixed(2).replace('.', ',')}</span>
        </div>
        <button class="cart-item-remove" onclick="removeFromCart(${idx})">✕</button>
      </div>`;
    });
    cartItemsEl.innerHTML = html;
    const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
    if (cartTotalEl) cartTotalEl.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
  }

  window.removeFromCart = function(idx) {
    cart.splice(idx, 1);
    saveCart();
    updateCartUI();
  };

  window.addToCart = function(name, price, icon) {
    const existing = cart.find(i => i.name === name);
    if (existing) { existing.qty++; }
    else { cart.push({ name, price, icon, qty: 1 }); }
    saveCart();
    updateCartUI();
    openCart();
  };

  updateCartUI();

  // ========== WHATSAPP CHECKOUT ==========
  window.whatsappCheckout = function() {
    if (cart.length === 0) return;
    const phone = '5567999128212';
    let msg = '🔑 *Pedido — Chaves de Sabedoria*\n\n';
    cart.forEach(item => {
      msg += `• ${item.name} (x${item.qty}) — R$ ${(item.price * item.qty).toFixed(2).replace('.', ',')}\n`;
    });
    const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
    msg += `\n💰 *Total: R$ ${total.toFixed(2).replace('.', ',')}*\n\nGostaria de finalizar este pedido!`;
    window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank');
  };

  // ========== LANGUAGE SYSTEM ==========
  const translations = {
    'pt': {
      'hero-title': 'Desbloqueie<br><span>Chaves</span> Diárias<br>de Sabedoria',
      'hero-sub': 'Uma experiência premium para quem busca direção, crescimento e soluções criativas com profundidade espiritual e excelência visual.',
      'btn-keys': 'Ver As Chaves',
      'btn-whatsapp': 'Falar no WhatsApp',
      'btn-substack': '<svg class="substack-icon" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/></svg> Assine Grátis e Receba 01 Chave por Dia',
      'keys-tag': 'As Chaves',
      'keys-title': 'Quatro dimensões de transformação',
      'keys-desc': 'Cada chave representa um desbloqueio estratégico para crescimento, posicionamento e clareza.',
      'products-tag': 'Loja',
      'products-title': 'Produtos Selecionados',
      'products-desc': 'Recursos premium para aprofundar sua jornada de sabedoria e transformação.',
      'faq-tag': 'Dúvidas',
      'faq-title': 'Perguntas Frequentes',
      'contact-tag': 'Contato',
      'contact-title': 'Pronto para desbloquear algo maior?',
    },
    'en': {
      'hero-title': 'Unlock<br>Daily <span>Keys</span><br>of Wisdom',
      'hero-sub': 'A premium experience for those seeking direction, growth and creative solutions with spiritual depth and visual excellence.',
      'btn-keys': 'See The Keys',
      'btn-whatsapp': 'Talk on WhatsApp',
      'btn-substack': '<svg class="substack-icon" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/></svg> Subscribe Free & Get 1 Key per Day',
      'keys-tag': 'The Keys',
      'keys-title': 'Four dimensions of transformation',
      'keys-desc': 'Each key represents a strategic unlock for growth, positioning and clarity.',
      'products-tag': 'Shop',
      'products-title': 'Selected Products',
      'products-desc': 'Premium resources to deepen your journey of wisdom and transformation.',
      'faq-tag': 'FAQ',
      'faq-title': 'Frequently Asked Questions',
      'contact-tag': 'Contact',
      'contact-title': 'Ready to unlock something greater?',
    },
    'es': {
      'hero-title': 'Desbloquea<br><span>Llaves</span> Diarias<br>de Sabiduría',
      'hero-sub': 'Una experiencia premium para quienes buscan dirección, crecimiento y soluciones creativas con profundidad espiritual y excelencia visual.',
      'btn-keys': 'Ver Las Llaves',
      'btn-whatsapp': 'Hablar en WhatsApp',
      'btn-substack': '<svg class="substack-icon" viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/></svg> Suscríbete Gratis y Recibe 1 Llave por Día',
      'keys-tag': 'Las Llaves',
      'keys-title': 'Cuatro dimensiones de transformación',
      'keys-desc': 'Cada llave representa un desbloqueo estratégico para crecimiento, posicionamiento y claridad.',
      'products-tag': 'Tienda',
      'products-title': 'Productos Seleccionados',
      'products-desc': 'Recursos premium para profundizar tu camino de sabiduría y transformación.',
      'faq-tag': 'Preguntas',
      'faq-title': 'Preguntas Frecuentes',
      'contact-tag': 'Contacto',
      'contact-title': '¿Listo para desbloquear algo mayor?',
    }
  };

  window.setLang = function(lang) {
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
    const t = translations[lang];
    if (!t) return;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      if (t[key]) el.innerHTML = t[key];
    });
    document.documentElement.lang = lang === 'pt' ? 'pt-BR' : lang;
  };

  // ========== BACK TO TOP ==========
  backTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ========== NEWSLETTER FORM ==========
  const nlForm = document.querySelector('.newsletter-form');
  nlForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = nlForm.querySelector('input');
    if (input?.value) {
      const phone = '5567999128212';
      const msg = `📧 Novo inscrito newsletter: ${input.value}`;
      window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank');
      input.value = '';
    }
  });

});
